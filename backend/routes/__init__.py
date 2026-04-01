# backend/routes/__init__.py
from flask import jsonify

def register_routes(app):
    """Register semua route ke app"""
    from routes.cluster import cluster_bp
    app.register_blueprint(cluster_bp, url_prefix='/api')
    
    # Health check
    @app.route('/api/health', methods=['GET'])
    def health():
        return jsonify({'status': 'ok', 'message': 'API is running'})