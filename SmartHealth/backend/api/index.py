from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        'status': 'ok',
        'message': 'SmartHealth Backend API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health-check',
            'register': '/api/auth/register',
            'login': '/api/auth/login'
        }
    })

@app.route('/api/health-check')
def health_check():
    return jsonify({'status': 'ok', 'message': 'SmartHealth API is running!'})

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    email = data.get('email', '')
    username = data.get('username', '')
    return jsonify({
        'message': 'Register endpoint working',
        'email': email,
        'username': username
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email', '')
    return jsonify({
        'message': 'Login endpoint working',
        'email': email
    })
