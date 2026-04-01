# backend/services/clustering_service.py
from utils.tfidf import create_tfidf_matrix
from utils.clustering import (
    find_optimal_k, perform_kmeans, get_cluster_centroids,
    get_cluster_summary, get_all_skills_with_score
)
from utils.evaluation import get_cluster_evaluation

def process_clustering(df, mode='auto', max_features=150, custom_k=None):
    """
    Proses clustering lengkap
    
    Returns:
        dict: Hasil clustering
    """
    # 1. TF-IDF
    X, vectorizer, feature_names = create_tfidf_matrix(df, max_features=max_features)
    
    # 2. Clustering
    if mode == 'auto':
        optimal_k, k_values, inertias, silhouettes = find_optimal_k(X, max_k=15)
        labels, model, silhouette = perform_kmeans(X, n_clusters=optimal_k)
        n_clusters = optimal_k
        elbow_data = {
            'k_values': k_values,
            'inertias': inertias,
            'silhouettes': silhouettes
        }
    else:
        labels, model, silhouette = perform_kmeans(X, n_clusters=custom_k)
        n_clusters = custom_k
        elbow_data = None
    
    # 3. Analisis Cluster
    centroids, top_skills_per_cluster = get_cluster_centroids(model, feature_names)
    all_skills_per_cluster = get_all_skills_with_score(model, feature_names)
    cluster_summary = get_cluster_summary(df, labels, top_skills_per_cluster)
    
    # 4. Evaluasi
    evaluation = get_cluster_evaluation(X, labels, n_clusters)
    
    # 5. Siapkan hasil
    result = {
        'success': True,
        'n_clusters': n_clusters,
        'n_samples': len(df),
        'evaluation': {
            'silhouette_score': evaluation['silhouette_score'],
            'davies_bouldin_score': evaluation['davies_bouldin_score'],
            'calinski_harabasz_score': evaluation['calinski_harabasz_score']
        },
        'clusters': [
            {
                'id': int(cluster_id),
                'name': summary['name'],
                'size': summary['size'],
                'percentage': summary['percentage'],
                'top_skills': [[skill, score] for skill, score in summary['top_skills']],
                'all_skills': all_skills_per_cluster[cluster_id],
                'sample_jobs': summary['sample_jobs']
            }
            for cluster_id, summary in cluster_summary.items()
        ],
        'jobs': [
            {
                'id': int(idx),
                'judul': row['judul'],
                'perusahaan': row.get('perusahaan', '-'),
                'platform': row.get('platform', '-'),
                'skills': row.get('skill_diekstrak', '').split(',') if row.get('skill_diekstrak') else [],
                'cluster': int(labels[idx]),
                'cluster_name': cluster_summary[labels[idx]]['name']
            }
            for idx, row in df.iterrows()
        ],
        'elbow_data': elbow_data,
        'mode': mode
    }
    
    return result