from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.supabase_client import get_supabase
from datetime import datetime

article_bp = Blueprint('article', __name__)

@article_bp.route('/articles', methods=['GET'])
def get_articles():
    article_type = request.args.get('type')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    offset = (page - 1) * limit
    
    try:
        supabase = get_supabase()
        query = supabase.table('health_articles').select('*').eq('publish_status', 'published').eq('audit_status', 'approved')
        
        if article_type:
            query = query.eq('article_type_id', article_type)
        
        response = query.order('created_at', desc=True).range(offset, offset + limit - 1).execute()
        
        return jsonify({
            'articles': response.data,
            'page': page,
            'limit': limit
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@article_bp.route('/articles/<article_id>', methods=['GET'])
def get_article(article_id):
    try:
        supabase = get_supabase()
        response = supabase.table('health_articles').select('*').eq('id', article_id).execute()
        
        if not response.data:
            return jsonify({'error': 'Article not found'}), 404
        
        return jsonify({
            'article': response.data[0]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@article_bp.route('/articles', methods=['POST'])
@jwt_required()
def create_article():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    article_data = {
        'title': data.get('title'),
        'content': data.get('content'),
        'cover_image': data.get('cover_image', ''),
        'article_type_id': data.get('article_type_id'),
        'author_id': user_id,
        'publish_status': 'draft',
        'audit_status': 'pending',
        'view_count': 0,
        'like_count': 0,
        'collect_count': 0,
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat()
    }
    
    try:
        supabase = get_supabase()
        response = supabase.table('health_articles').insert(article_data).execute()
        return jsonify({
            'message': 'Article created successfully',
            'article': response.data[0]
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@article_bp.route('/types', methods=['GET'])
def get_article_types():
    try:
        supabase = get_supabase()
        response = supabase.table('article_types').select('*').order('sort').execute()
        return jsonify({
            'types': response.data
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
