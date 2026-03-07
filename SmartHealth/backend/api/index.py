from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        'status': 'ok',
        'message': 'SmartHealth Backend API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health-check',
            'auth_register': '/api/auth/register',
            'auth_login': '/api/auth/login'
        'diet_records': '/api/diet/records',
            'exercise_records': '/api/exercise/records',
            'ai_analyze': '/api/ai/analyze'
        }
    })

@app.route('/api/health-check')
def health_check():
    return jsonify({'status': 'ok', 'message': 'SmartHealth API is running!'})

@app.route('/api/auth/register', methods=['POST'])
def auth_register():
    return jsonify({'message': 'Register endpoint working'})

@app.route('/api/auth/login', methods=['POST'])
def auth_login():
    return jsonify({'message': 'Login endpoint working'})
