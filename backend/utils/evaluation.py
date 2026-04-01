# backend/utils/evaluation.py
import numpy as np
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score

def get_cluster_evaluation(X, labels, n_clusters):
    """
    Mendapatkan berbagai metrik evaluasi clustering
    """
    X_array = X.toarray() if hasattr(X, 'toarray') else X
    
    evaluation = {
        'n_clusters': n_clusters,
        'n_samples': len(labels),
        'silhouette_score': None,
        'davies_bouldin_score': None,
        'calinski_harabasz_score': None,
        'cluster_distribution': dict(zip(*np.unique(labels, return_counts=True)))
    }
    
    if n_clusters >= 2 and len(np.unique(labels)) >= 2:
        evaluation['silhouette_score'] = silhouette_score(X_array, labels)
        evaluation['davies_bouldin_score'] = davies_bouldin_score(X_array, labels)
        evaluation['calinski_harabasz_score'] = calinski_harabasz_score(X_array, labels)
    
    return evaluation