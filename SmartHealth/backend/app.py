from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    CORS(app, origins=app.config['CORS_ORIGINS'])
    JWTManager(app)
    
    from app.routes.auth import auth_bp
    from app.routes.health import health_bp
    from app.routes.diet import diet_bp
    from app.routes.exercise import exercise_bp
    from app.routes.article import article_bp
    from app.routes.ai import ai_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(health_bp, url_prefix='/api/health')
    app.register_blueprint(diet_bp, url_prefix='/api/diet')
    app.register_blueprint(exercise_bp, url_prefix='/api/exercise')
    app.register_blueprint(article_bp, url_prefix='/api/article')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    
    @app.route('/api/health-check')
    def health_check():
        return {'status': 'ok', 'message': 'SmartHealth API is running!'}
    
    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    app.run(host='0.0.0.0', port=5000, debug=True)
