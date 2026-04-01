# backend/utils/tfidf.py
from sklearn.feature_extraction.text import TfidfVectorizer
from utils.preprocessing import get_skill_string_corpus

def create_tfidf_matrix(df, max_features=150):
    """
    Membuat matriks TF-IDF
    
    Returns:
        X: matriks TF-IDF (sparse matrix)
        vectorizer: objek TfidfVectorizer
        feature_names: daftar kata kunci (skills)
    """
    text_corpus = get_skill_string_corpus(df)
    
    vectorizer = TfidfVectorizer(
        token_pattern=r'(?u)\b\w+\b',
        lowercase=True,
        max_features=max_features,
        stop_words=None
    )
    
    X = vectorizer.fit_transform(text_corpus)
    feature_names = vectorizer.get_feature_names_out()
    
    return X, vectorizer, feature_names