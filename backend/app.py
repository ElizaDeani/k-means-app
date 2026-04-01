# backend/app.py
from flask import Flask
from flask_cors import CORS
from config import Config
from routes import register_routes

# Inisialisasi Flask
app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS (izin frontend panggil API)
# CORS configuration - allow all origins for development
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Register semua route
register_routes(app)

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 API Server Starting...")
    print("="*50)
    print(f"📍 Default dataset: {Config.DEFAULT_DATASET}")
    print(f"📍 Upload folder: {Config.UPLOAD_FOLDER}")
    print(f"📍 Health check: http://localhost:{Config.PORT}/api/health")
    print(f"📍 Cluster endpoint: http://localhost:{Config.PORT}/api/cluster")
    print("="*50 + "\n")
    
    app.run(
        debug=Config.DEBUG,
        host=Config.HOST,
        port=Config.PORT
    )