from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        'status': 'ok',
        'message': 'SmartHealth Backend API',
        'version': '1.0.0'
    })

@app.route('/api/health-check')
def health_check():
    return jsonify({
        'status': 'ok',
        'message': 'SmartHealth API is running!'
    })

@app.route('/api/auth/register', methods=['POST'])
def register():
    return jsonify({'message': 'Register endpoint'})

@app.route('/api/auth/login', methods=['POST'])
def login():
    return jsonify({'message': 'Login endpoint'})
