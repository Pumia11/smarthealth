from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.supabase_client import supabase
from datetime import datetime

diet_bp = Blueprint('diet', __name__)

@diet_bp.route('/foods', methods=['GET'])
@jwt_required()
def get_foods():
    food_type_id = request.args.get('type_id')
    search = request.args.get('search')
    
    try:
        query = supabase.table('foods').select('''
            *,
            food_type:food_types(id, name)
        ''')
        
        if food_type_id:
            query = query.eq('food_type_id', food_type_id)
        if search:
            query = query.ilike('name', f'%{search}%')
            
        response = query.order('name').execute()
        
        return jsonify({
            'foods': response.data
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@diet_bp.route('/food-types', methods=['GET'])
def get_food_types():
    try:
        response = supabase.table('food_types').select('*').order('sort').execute()
        return jsonify({
            'types': response.data
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@diet_bp.route('/records', methods=['GET'])
@jwt_required()
def get_records():
    user_id = get_jwt_identity()
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    meal_type = request.args.get('meal_type')
    
    try:
        query = supabase.table('diet_records').select('''
            *,
            food:foods(id, name, calories, protein, carbohydrates, fat)
        ''').eq('user_id', user_id)
        
        if start_date:
            query = query.gte('record_time', start_date)
        if end_date:
            query = query.lte('record_time', end_date)
        if meal_type:
            query = query.eq('meal_type', meal_type)
            
        response = query.order('record_time', desc=True).execute()
        
        return jsonify({
            'records': response.data
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@diet_bp.route('/records', methods=['POST'])
@jwt_required()
def create_record():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    food_id = data.get('food_id')
    weight = data.get('weight')
    meal_type = data.get('meal_type')
    record_time = data.get('record_time', datetime.utcnow().isoformat())
    remark = data.get('remark', '')
    
    try:
        food_response = supabase.table('foods').select('*').eq('id', food_id).execute()
        
        if not food_response.data:
            return jsonify({'error': 'Food not found'}), 404
        
        food = food_response.data[0]
        multiplier = weight / 100
        
        record_data = {
            'user_id': user_id,
            'food_id': food_id,
            'meal_type': meal_type,
            'weight': weight,
            'total_calories': round(food['calories'] * multiplier, 2),
            'total_protein': round(food.get('protein', 0) * multiplier, 2),
            'total_carbs': round(food.get('carbohydrates', 0) * multiplier, 2),
            'total_fat': round(food.get('fat', 0) * multiplier, 2),
            'record_time': record_time,
            'remark': remark,
            'created_at': datetime.utcnow().isoformat()
        }
        
        response = supabase.table('diet_records').insert(record_data).execute()
        
        return jsonify({
            'message': 'Diet record created successfully',
            'record': response.data[0]
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@diet_bp.route('/stats/daily', methods=['GET'])
@jwt_required()
def get_daily_stats():
    user_id = get_jwt_identity()
    date = request.args.get('date', datetime.utcnow().strftime('%Y-%m-%d'))
    
    try:
        response = supabase.table('diet_records').select('''
            total_calories, total_protein, total_carbs, total_fat, meal_type
        ''').eq('user_id', user_id).gte('record_time', f'{date}T00:00:00').lte('record_time', f'{date}T23:59:59').execute()
        
        stats = {
            'total_calories': 0,
            'total_protein': 0,
            'total_carbs': 0,
            'total_fat': 0,
            'by_meal': {
                'breakfast': {'calories': 0, 'count': 0},
                'lunch': {'calories': 0, 'count': 0},
                'dinner': {'calories': 0, 'count': 0},
                'snack': {'calories': 0, 'count': 0}
            }
        }
        
        for record in response.data:
            stats['total_calories'] += record['total_calories']
            stats['total_protein'] += record['total_protein']
            stats['total_carbs'] += record['total_carbs']
            stats['total_fat'] += record['total_fat']
            
            meal = record['meal_type']
            if meal in stats['by_meal']:
                stats['by_meal'][meal]['calories'] += record['total_calories']
                stats['by_meal'][meal]['count'] += 1
        
        return jsonify({
            'date': date,
            'stats': stats
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
