from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.supabase_client import get_supabase
from datetime import datetime

exercise_bp = Blueprint('exercise', __name__)

@exercise_bp.route('/exercises', methods=['GET'])
@jwt_required()
def get_exercises():
    exercise_type_id = request.args.get('type_id')
    search = request.args.get('search')
    
    try:
        supabase = get_supabase()
        query = supabase.table('exercises').select('''
            *,
            exercise_type:exercise_types(id, name)
        ''')
        
        if exercise_type_id:
            query = query.eq('exercise_type_id', exercise_type_id)
        if search:
            query = query.ilike('name', f'%{search}%')
            
        response = query.order('name').execute()
        
        return jsonify({
            'exercises': response.data
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@exercise_bp.route('/exercise-types', methods=['GET'])
def get_exercise_types():
    try:
        supabase = get_supabase()
        response = supabase.table('exercise_types').select('*').order('sort').execute()
        return jsonify({
            'types': response.data
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@exercise_bp.route('/records', methods=['GET'])
@jwt_required()
def get_records():
    user_id = get_jwt_identity()
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    try:
        supabase = get_supabase()
        query = supabase.table('exercise_records').select('''
            *,
            exercise:exercises(id, name, mets, cover_image)
        ''').eq('user_id', user_id)
        
        if start_date:
            query = query.gte('record_time', start_date)
        if end_date:
            query = query.lte('record_time', end_date)
            
        response = query.order('record_time', desc=True).execute()
        
        return jsonify({
            'records': response.data
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@exercise_bp.route('/records', methods=['POST'])
@jwt_required()
def create_record():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    exercise_id = data.get('exercise_id')
    duration = data.get('duration')
    record_time = data.get('record_time', datetime.utcnow().isoformat())
    heart_rate_avg = data.get('heart_rate_avg')
    heart_rate_max = data.get('heart_rate_max')
    remark = data.get('remark', '')
    
    try:
        supabase = get_supabase()
        user_response = supabase.table('user_profiles').select('weight').eq('user_id', user_id).execute()
        weight = user_response.data[0]['weight'] if user_response.data else 65
        
        exercise_response = supabase.table('exercises').select('*').eq('id', exercise_id).execute()
        
        if not exercise_response.data:
            return jsonify({'error': 'Exercise not found'}), 404
        
        exercise = exercise_response.data[0]
        mets = exercise.get('mets', 1.0)
        calories_burned = round(mets * weight * (duration / 60), 2)
        
        record_data = {
            'user_id': user_id,
            'exercise_id': exercise_id,
            'duration': duration,
            'calories_burned': calories_burned,
            'record_time': record_time,
            'heart_rate_avg': heart_rate_avg,
            'heart_rate_max': heart_rate_max,
            'remark': remark,
            'created_at': datetime.utcnow().isoformat()
        }
        
        response = supabase.table('exercise_records').insert(record_data).execute()
        
        return jsonify({
            'message': 'Exercise record created successfully',
            'record': response.data[0],
            'calories_burned': calories_burned
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@exercise_bp.route('/stats/daily', methods=['GET'])
@jwt_required()
def get_daily_stats():
    user_id = get_jwt_identity()
    date = request.args.get('date', datetime.utcnow().strftime('%Y-%m-%d'))
    
    try:
        supabase = get_supabase()
        response = supabase.table('exercise_records').select('''
            duration, calories_burned, exercise:exercises(name)
        ''').eq('user_id', user_id).gte('record_time', f'{date}T00:00:00').lte('record_time', f'{date}T23:59:59').execute()
        
        stats = {
            'total_duration': 0,
            'total_calories': 0,
            'exercise_count': len(response.data),
            'exercises': []
        }
        
        for record in response.data:
            stats['total_duration'] += record['duration']
            stats['total_calories'] += record['calories_burned']
            stats['exercises'].append({
                'name': record['exercise']['name'],
                'duration': record['duration'],
                'calories': record['calories_burned']
            })
        
        return jsonify({
            'date': date,
            'stats': stats
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
