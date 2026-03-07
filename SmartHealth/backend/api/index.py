from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        'status': 'ok',
        'message': 'SmartHealth Backend API is running!',
        'version': '1.0.0'
    })

@app.route('/api/health-check')
def health_check():
    return jsonify({'status': 'ok', 'message': 'API is healthy!'})
