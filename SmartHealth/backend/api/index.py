import os
import sys
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from dotenv import load_dotenv
from supabase import create_client, Client
import requests
import json
from datetime import datetime, timedelta
from functools import wraps

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'smarthealth-secret-2024')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')

CORS(app, origins='*')
JWTManager(app)

_supabase_client = None

def get_supabase():
    global _supabase_client
    if _supabase_client is None:
        url = os.environ.get('SUPABASE_URL')
        key = os.environ.get('SUPABASE_KEY')
        if url and key:
            _supabase_client = create_client(url, key)
    return _supabase_client

def validate_email(email):
    import re
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is not None

@app.route('/')
def index():
    return jsonify({
        'status': 'ok',
        'message': 'SmartHealth Backend API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health-check',
            'register': '/api/auth/register',
            'login': '/api/auth/login',
            'profile': '/api/auth/me'
        }
    })

@app.route('/api/health-check')
def health_check():
    return jsonify({'status': 'ok', 'message': 'SmartHealth API is running!'})

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    email = data.get('email', '')
    password = data.get('password', '')
    username = data.get('username', '')
    
    if not email or not password or not username:
        return jsonify({'error': 'Missing required fields'}), 400
    
    if not validate_email(email):
        return jsonify({'error': 'Invalid email format'}), 400
    
    if len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters'}), 400
    
    supabase = get_supabase()
    if not supabase:
        return jsonify({'error': 'Database not configured'}), 500
    
    try:
        response = supabase.auth.sign_up({
            'email': email,
            'password': password,
            'options': {
                'data': {
                    'username': username
                }
            }
        })
        
        if response.user:
            return jsonify({
                'message': 'User registered successfully',
                'user': {
                    'id': response.user.id,
                    'email': response.user.email,
                    'username': username
                }
            }), 201
        else:
            return jsonify({'error': 'Registration failed'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email', '')
    password = data.get('password', '')
    
    if not email or not password:
        return jsonify({'error': 'Missing email or password'}), 400
    
    supabase = get_supabase()
    if not supabase:
        return jsonify({'error': 'Database not configured'}), 500
    
    try:
        response = supabase.auth.sign_in_with_password({
            'email': email,
            'password': password
        })
        
        if response.user:
            access_token = create_access_token(identity=response.user.id)
            return jsonify({
                'message': 'Login successful',
                'access_token': access_token,
                'user': {
                    'id': response.user.id,
                    'email': response.user.email,
                    'username': response.user.user_metadata.get('username', '')
                }
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 401

@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    supabase = get_supabase()
    
    if not supabase:
        return jsonify({'error': 'Database not configured'}), 500
    
    try:
        response = supabase.table('user_profiles').select('*').eq('user_id', user_id).execute()
        
        if response.data:
            return jsonify({'user': response.data[0]}), 200
        else:
            return jsonify({'user': {'id': user_id}}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/me', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    
    supabase = get_supabase()
    if not supabase:
        return jsonify({'error': 'Database not configured'}), 500
    
    try:
        response = supabase.table('user_profiles').update(data).eq('user_id', user_id).execute()
        return jsonify({'message': 'Profile updated', 'user': response.data[0] if response.data else {}}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

MINIMAX_API_KEY = os.environ.get('MINIMAX_API_KEY')
MINIMAX_GROUP_ID = os.environ.get('MINIMAX_GROUP_ID')

@app.route('/api/ai/analyze', methods=['POST'])
@jwt_required()
def ai_analyze():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    days = data.get('days', 7)
    
    supabase = get_supabase()
    if not supabase:
        return jsonify({'error': 'Database not configured'}), 500
    
    try:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        health_records = supabase.table('health_records').select('*').eq('user_id', user_id).gte('record_time', start_date.isoformat()).execute()
        diet_records = supabase.table('diet_records').select('*').eq('user_id', user_id).gte('record_time', start_date.isoformat()).execute()
        exercise_records = supabase.table('exercise_records').select('*').eq('user_id', user_id).gte('record_time', start_date.isoformat()).execute()
        
        analysis_result = {
            'health_score': 75,
            'risks': ['建议增加运动频率', '注意饮食均衡'],
            'nutrition_analysis': {
                'calories_status': '日均摄入适中',
                'suggestions': ['建议增加蔬菜水果摄入']
            },
            'exercise_analysis': {
                'total_duration': sum(r.get('duration', 0) for r in exercise_records.data),
                'suggestions': ['建议每周运动3-5次']
            },
            'recommendations': ['保持规律作息', '多喝水', '定期体检']
        }
        
        if MINIMAX_API_KEY and MINIMAX_GROUP_ID:
            try:
                prompt = f"分析用户健康数据：健康记录{len(health_records.data)}条，饮食记录{len(diet_records.data)}条，运动记录{len(exercise_records.data)}条。请提供健康建议。"
                response = requests.post(
                    'https://api.minimax.chat/v1/text/chatcompletion_v2',
                    headers={'Authorization': f'Bearer {MINIMAX_API_KEY}'},
                    json={
                        'model': 'abab6.5s-chat',
                        'messages': [
                            {'role': 'system', 'content': '你是健康分析师'},
                            {'role': 'user', 'content': prompt}
                        ]
                    },
                    timeout=30
                )
                if response.status_code == 200:
                    result = response.json()
                    analysis_result['ai_insight'] = result['choices'][0]['message']['content']
            except:
                pass
        
        return jsonify({'message': 'Analysis completed', 'analysis': analysis_result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health/indicators', methods=['GET'])
@jwt_required()
def get_health_indicators():
    supabase = get_supabase()
    if not supabase:
        return jsonify({'error': 'Database not configured'}), 500
    
    try:
        response = supabase.table('health_indicators').select('*').eq('status', True).execute()
        return jsonify({'indicators': response.data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health/records', methods=['GET'])
@jwt_required()
def get_health_records():
    user_id = get_jwt_identity()
    supabase = get_supabase()
    
    if not supabase:
        return jsonify({'error': 'Database not configured'}), 500
    
    try:
        response = supabase.table('health_records').select('*').eq('user_id', user_id).order('record_time', desc=True).execute()
        return jsonify({'records': response.data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health/records', methods=['POST'])
@jwt_required()
def create_health_record():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    
    supabase = get_supabase()
    if not supabase:
        return jsonify({'error': 'Database not configured'}), 500
    
    try:
        record_data = {
            'user_id': user_id,
            'indicator_id': data.get('indicator_id'),
            'value': data.get('value'),
            'record_time': data.get('record_time', datetime.utcnow().isoformat()),
            'remark': data.get('remark', ''),
            'source': 'manual'
        }
        response = supabase.table('health_records').insert(record_data).execute()
        return jsonify({'message': 'Record created', 'record': response.data[0]}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/diet/records', methods=['GET'])
@jwt_required()
def get_diet_records():
    user_id = get_jwt_identity()
    supabase = get_supabase()
    
    if not supabase:
        return jsonify({'error': 'Database not configured'}), 500
    
    try:
        response = supabase.table('diet_records').select('*').eq('user_id', user_id).order('record_time', desc=True).execute()
        return jsonify({'records': response.data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/diet/records', methods=['POST'])
@jwt_required()
def create_diet_record():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    
    supabase = get_supabase()
    if not supabase:
        return jsonify({'error': 'Database not configured'}), 500
    
    try:
        record_data = {
            'user_id': user_id,
            'food_id': data.get('food_id'),
            'meal_type': data.get('meal_type'),
            'weight': data.get('weight'),
            'total_calories': data.get('total_calories', 0),
            'record_time': data.get('record_time', datetime.utcnow().isoformat()),
            'remark': data.get('remark', '')
        }
        response = supabase.table('diet_records').insert(record_data).execute()
        return jsonify({'message': 'Record created', 'record': response.data[0]}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/exercise/records', methods=['GET'])
@jwt_required()
def get_exercise_records():
    user_id = get_jwt_identity()
    supabase = get_supabase()
    
    if not supabase:
        return jsonify({'error': 'Database not configured'}), 500
    
    try:
        response = supabase.table('exercise_records').select('*').eq('user_id', user_id).order('record_time', desc=True).execute()
        return jsonify({'records': response.data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/exercise/records', methods=['POST'])
@jwt_required()
def create_exercise_record():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    
    supabase = get_supabase()
    if not supabase:
        return jsonify({'error': 'Database not configured'}), 500
    
    try:
        record_data = {
            'user_id': user_id,
            'exercise_id': data.get('exercise_id'),
            'duration': data.get('duration'),
            'calories_burned': data.get('calories_burned', 0),
            'record_time': data.get('record_time', datetime.utcnow().isoformat()),
            'remark': data.get('remark', '')
        }
        response = supabase.table('exercise_records').insert(record_data).execute()
        return jsonify({'message': 'Record created', 'record': response.data[0]}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500
