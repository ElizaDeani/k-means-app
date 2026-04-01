# backend/config.py
import os

class Config:
    """Konfigurasi aplikasi"""
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    
    # File default dataset
    DEFAULT_DATASET = os.path.join(DATA_DIR, 'dataset.xlsx')
    
    # Parameter default
    DEFAULT_MAX_FEATURES = 150
    DEFAULT_MAX_K = 15
    
    # Flask
    SECRET_KEY = 'skripsi-deepy-2024'
    DEBUG = True
    PORT = 5000
    HOST = '0.0.0.0'

# Buat folder jika belum ada
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(Config.DATA_DIR, exist_ok=True)