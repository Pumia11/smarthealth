from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.supabase_client import get_supabase
from ..services.ai_service import analyze_health
from datetime import datetime, timedelta

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/analyze', methods=['POST'])
@jwt_required()
def analyze():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    days = data.get('days', 7)
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    try:
        supabase = get_supabase()
        health_records = supabase.table('health_records').select('''
            value, record_time, is_abnormal,
            indicator:health_indicators(name, unit, normal_min, normal_max)
        ''').eq('user_id', user_id).gte('record_time', start_date.isoformat()).order('record_time', desc=True).execute()
        
        diet_records = supabase.table('diet_records').select('''
            total_calories, total_protein, total_carbs, total_fat, 
            record_time, meal_type,
            food:foods(name)
        ''').eq('user_id', user_id).gte('record_time', start_date.isoformat()).order('record_time', desc=True).execute()
        
        exercise_records = supabase.table('exercise_records').select('''
            duration, calories_burned, record_time,
            exercise:exercises(name, mets)
        ''').eq('user_id', user_id).gte('record_time', start_date.isoformat()).order('record_time', desc=True).execute()
        
        user_profile = supabase.table('user_profiles').select('*').eq('user_id', user_id).execute()
        
        analysis_data = {
            'user_profile': user_profile.data[0] if user_profile.data else {},
            'health_records': health_records.data,
            'diet_records': diet_records.data,
            'exercise_records': exercise_records.data,
            'analysis_period': {
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'days': days
            }
        }
        
        analysis_result = analyze_health(analysis_data)
        
        report_data = {
            'user_id': user_id,
            'analysis_type': 'comprehensive',
            'analysis_period_days': days,
            'health_score': analysis_result.get('health_score', 0),
            'risks': analysis_result.get('risks', []),
            'nutrition_analysis': analysis_result.get('nutrition_analysis', {}),
            'exercise_analysis': analysis_result.get('exercise_analysis', {}),
            'indicator_analysis': analysis_result.get('indicator_analysis', {}),
            'recommendations': analysis_result.get('recommendations', []),
            'created_at': datetime.utcnow().isoformat()
        }
        
        supabase.table('health_reports').insert(report_data).execute()
        
        return jsonify({
            'message': 'Analysis completed successfully',
            'analysis': analysis_result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/reports', methods=['GET'])
@jwt_required()
def get_reports():
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    offset = (page - 1) * limit
    
    try:
        supabase = get_supabase()
        response = supabase.table('health_reports').select('*').eq('user_id', user_id).order('created_at', desc=True).range(offset, offset + limit - 1).execute()
        
        return jsonify({
            'reports': response.data,
            'page': page,
            'limit': limit
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/reports/<report_id>', methods=['GET'])
@jwt_required()
def get_report(report_id):
    user_id = get_jwt_identity()
    
    try:
        supabase = get_supabase()
        response = supabase.table('health_reports').select('*').eq('id', report_id).eq('user_id', user_id).execute()
        
        if not response.data:
            return jsonify({'error': 'Report not found'}), 404
        
        return jsonify({
            'report': response.data[0]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
