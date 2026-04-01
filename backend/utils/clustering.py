# backend/utils/clustering.py
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def find_optimal_k(X, max_k=15):
    """
    Menentukan K optimal menggunakan Elbow Method
    """
    max_k = min(max_k, X.shape[0] - 1)
    
    k_values = range(2, max_k + 1)
    inertias = []
    silhouettes = []
    
    for k in k_values:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X)
        inertias.append(kmeans.inertia_)
        
        if X.shape[0] > k:
            silhouette = silhouette_score(X, kmeans.labels_)
            silhouettes.append(silhouette)
        else:
            silhouettes.append(-1)
    
    # Cari titik elbow (penurunan inertia terbesar)
    inertia_diffs = []
    for i in range(1, len(inertias)):
        diff = inertias[i-1] - inertias[i]
        inertia_diffs.append(diff)
    
    if inertia_diffs:
        elbow_index = np.argmax(inertia_diffs)
        optimal_k = k_values[elbow_index]
    else:
        optimal_k = 3
    
    return optimal_k, list(k_values), inertias, silhouettes

def perform_kmeans(X, n_clusters=3, random_state=42):
    """
    Melakukan clustering K-Means
    """
    model = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
    labels = model.fit_predict(X)
    silhouette = silhouette_score(X, labels) if n_clusters >= 2 else None
    return labels, model, silhouette

def get_cluster_centroids(model, feature_names):
    """
    Mendapatkan centroid dan top skills per cluster
    """
    centroids = model.cluster_centers_
    
    top_skills_per_cluster = {}
    for cluster_idx in range(len(centroids)):
        centroid = centroids[cluster_idx]
        top_indices = np.argsort(centroid)[::-1][:10]
        top_skills = [(feature_names[i], centroid[i]) for i in top_indices]
        top_skills_per_cluster[cluster_idx] = top_skills
    
    return centroids, top_skills_per_cluster

def get_all_skills_with_score(model, feature_names):
    """
    Mendapatkan semua skill dengan bobot untuk setiap cluster
    """
    centroids = model.cluster_centers_
    
    all_skills_per_cluster = {}
    for cluster_idx in range(len(centroids)):
        centroid = centroids[cluster_idx]
        skill_scores = {feature_names[i]: centroid[i] for i in range(len(feature_names)) if centroid[i] > 0}
        skill_scores = dict(sorted(skill_scores.items(), key=lambda x: x[1], reverse=True))
        all_skills_per_cluster[cluster_idx] = skill_scores
    
    return all_skills_per_cluster

def suggest_cluster_name(top_skills):
    """
    Menentukan nama cluster berdasarkan top skills
    """
    frontend_keywords = ['react', 'vue', 'angular', 'javascript', 'typescript', 'html', 'css', 'tailwind', 'bootstrap', 'next.js', 'redux']
    backend_keywords = ['java', 'golang', 'python', 'node', 'php', 'laravel', 'spring', 'django', 'postgresql', 'mysql', 'mongodb']
    devops_keywords = ['docker', 'kubernetes', 'aws', 'gcp', 'azure', 'ci/cd', 'jenkins', 'terraform']
    
    top_skills_lower = [s.lower() for s in top_skills[:5]]
    
    frontend_count = sum(1 for skill in top_skills_lower if skill in frontend_keywords)
    backend_count = sum(1 for skill in top_skills_lower if skill in backend_keywords)
    devops_count = sum(1 for skill in top_skills_lower if skill in devops_keywords)
    
    if frontend_count >= 2 and backend_count < 2:
        return "Frontend Developer"
    elif backend_count >= 2 and frontend_count < 2:
        return "Backend Developer"
    elif devops_count >= 2:
        return "DevOps / Cloud Engineer"
    elif frontend_count >= 2 and backend_count >= 2:
        return "Fullstack Developer"
    else:
        return f"{top_skills[0].title()} Developer"

def get_cluster_summary(df, labels, top_skills_per_cluster):
    """
    Membuat summary untuk setiap cluster
    """
    summary = {}
    unique_clusters = np.unique(labels)
    
    for cluster in unique_clusters:
        cluster_indices = np.where(labels == cluster)[0]
        cluster_data = df.iloc[cluster_indices]
        
        top_skills = [skill for skill, _ in top_skills_per_cluster[cluster][:3]]
        cluster_name = suggest_cluster_name(top_skills)
        
        summary[cluster] = {
            'name': cluster_name,
            'size': len(cluster_indices),
            'percentage': (len(cluster_indices) / len(df)) * 100,
            'top_skills': top_skills_per_cluster[cluster],
            'sample_jobs': cluster_data['judul'].head(5).tolist()
        }
    
    return summary