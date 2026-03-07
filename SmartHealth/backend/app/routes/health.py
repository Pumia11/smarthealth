from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.supabase_client import supabase
from datetime import datetime

health_bp = Blueprint('health', __name__)

@health_bp.route('/indicators', methods=['GET'])
@jwt_required()
def get_indicators():
    user_id = get_jwt_identity()
    
    try:
        response = supabase.table('health_indicators').select('''
            *,
            indicator_type:health_indicator_types(id, name)
        ''').or_(f'belong_user_id.eq.{user_id},is_common.eq.true').execute()
        
        return jsonify({
            'indicators': response.data
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@health_bp.route('/indicators', methods=['POST'])
@jwt_required()
def create_indicator():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    indicator_data = {
        'name': data.get('name'),
        'indicator_type_id': data.get('indicator_type_id'),
        'belong_user_id': user_id,
        'unit': data.get('unit', ''),
        'normal_min': data.get('normal_min'),
        'normal_max': data.get('normal_max'),
        'threshold_desc': data.get('threshold_desc', ''),
        'is_common': False,
        'created_at': datetime.utcnow().isoformat()
    }
    
    try:
        response = supabase.table('health_indicators').insert(indicator_data).execute()
        return jsonify({
            'message': 'Indicator created successfully',
            'indicator': response.data[0]
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@health_bp.route('/records', methods=['GET'])
@jwt_required()
def get_records():
    user_id = get_jwt_identity()
    indicator_id = request.args.get('indicator_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    try:
        query = supabase.table('health_records').select('''
            *,
            indicator:health_indicators(id, name, unit)
        ''').eq('user_id', user_id)
        
        if indicator_id:
            query = query.eq('indicator_id', indicator_id)
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

@health_bp.route('/records', methods=['POST'])
@jwt_required()
def create_record():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    indicator_id = data.get('indicator_id')
    value = data.get('value')
    record_time = data.get('record_time', datetime.utcnow().isoformat())
    remark = data.get('remark', '')
    
    try:
        indicator_response = supabase.table('health_indicators').select('normal_min, normal_max').eq('id', indicator_id).execute()
        
        is_abnormal = False
        if indicator_response.data:
            indicator = indicator_response.data[0]
            if indicator.get('normal_min') and indicator.get('normal_max'):
                is_abnormal = not (indicator['normal_min'] <= value <= indicator['normal_max'])
        
        record_data = {
            'user_id': user_id,
            'indicator_id': indicator_id,
            'value': value,
            'record_time': record_time,
            'is_abnormal': is_abnormal,
            'remark': remark,
            'source': 'manual',
            'created_at': datetime.utcnow().isoformat()
        }
        
        response = supabase.table('health_records').insert(record_data).execute()
        
        return jsonify({
            'message': 'Record created successfully',
            'record': response.data[0],
            'is_abnormal': is_abnormal
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@health_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    user_id = get_jwt_identity()
    
    try:
        records_response = supabase.table('health_records').select('''
            *,
            indicator:health_indicators(id, name, unit)
        ''').eq('user_id', user_id).order('record_time', desc=True).limit(100).execute()
        
        stats = {}
        for record in records_response.data:
            indicator_name = record['indicator']['name']
            if indicator_name not in stats:
                stats[indicator_name] = {
                    'latest': record['value'],
                    'unit': record['indicator']['unit'],
                    'is_abnormal': record['is_abnormal'],
                    'record_time': record['record_time']
                }
        
        return jsonify({
            'stats': stats
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
