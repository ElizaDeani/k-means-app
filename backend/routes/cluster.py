# backend/routes/cluster.py
from flask import request, jsonify, Blueprint
from services.data_service import get_dataframe
from services.clustering_service import process_clustering

# Buat blueprint
cluster_bp = Blueprint('cluster', __name__)

@cluster_bp.route('/cluster', methods=['POST'])
def cluster():
    """
    Endpoint clustering
    
    Request (form-data):
        - file: file Excel (optional)
        - mode: 'auto' atau 'manual'
        - k: jumlah cluster (jika mode manual)
        - max_features: maksimal fitur (default 150)
    """
    try:
        # Ambil parameter
        mode = request.form.get('mode', 'auto')
        max_features = int(request.form.get('max_features', 150))
        custom_k = int(request.form.get('k', 3)) if mode == 'manual' else None
        
        print(f"[INFO] Mode: {mode}, Max Features: {max_features}")
        if mode == 'manual':
            print(f"[INFO] Custom K: {custom_k}")
        
        # Load data
        file = request.files.get('file')
        df, filepath = get_dataframe(file)
        
        print(f"[INFO] Loaded {len(df)} jobs from {filepath}")
        
        # Proses clustering
        result = process_clustering(df, mode, max_features, custom_k)
        
        return jsonify(result)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500