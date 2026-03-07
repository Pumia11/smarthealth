from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from ..services.supabase_client import get_supabase
from ..utils.validators import validate_email, validate_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    
    if not email or not password or not username:
        return jsonify({'error': 'Missing required fields'}), 400
    
    if not validate_email(email):
        return jsonify({'error': 'Invalid email format'}), 400
    
    if not validate_password(password):
        return jsonify({'error': 'Password must be at least 8 characters'}), 400
    
    try:
        supabase = get_supabase()
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

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Missing email or password'}), 400
    
    try:
        supabase = get_supabase()
        response = supabase.auth.sign_in_with_password({
            'email': email,
            'password': password
        })
        
        if response.user:
            access_token = create_access_token(identity=response.user.id)
            refresh_token = create_refresh_token(identity=response.user.id)
            
            return jsonify({
                'message': 'Login successful',
                'access_token': access_token,
                'refresh_token': refresh_token,
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

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    access_token = create_access_token(identity=current_user_id)
    
    return jsonify({
        'access_token': access_token
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    
    try:
        supabase = get_supabase()
        response = supabase.auth.get_user()
        
        if response.user:
            return jsonify({
                'user': {
                    'id': response.user.id,
                    'email': response.user.email,
                    'username': response.user.user_metadata.get('username', ''),
                    'avatar': response.user.user_metadata.get('avatar', ''),
                    'gender': response.user.user_metadata.get('gender', ''),
                    'birthday': response.user.user_metadata.get('birthday', ''),
                    'height': response.user.user_metadata.get('height', 0),
                    'weight': response.user.user_metadata.get('weight', 0)
                }
            }), 200
        else:
            return jsonify({'error': 'User not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    try:
        supabase = get_supabase()
        response = supabase.auth.update_user({
            'data': data
        })
        
        if response.user:
            return jsonify({
                'message': 'Profile updated successfully',
                'user': {
                    'id': response.user.id,
                    'email': response.user.email,
                    **response.user.user_metadata
                }
            }), 200
        else:
            return jsonify({'error': 'Update failed'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        supabase = get_supabase()
        supabase.auth.sign_out()
        return jsonify({'message': 'Logged out successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
