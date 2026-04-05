from flask import Flask, send_from_directory
from flask_cors import CORS
from config import Config
from routes import register_routes
import os

# ✅ 1. BUAT APP DULU
app = Flask(__name__)
app.config.from_object(Config)

# ✅ 2. PATH FRONTEND
FRONTEND_FOLDER = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../frontend')
)

# ✅ 3. ROUTE FRONTEND
@app.route('/')
def index():
    return send_from_directory(FRONTEND_FOLDER, 'capek.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(FRONTEND_FOLDER, path)

# ✅ 4. CORS
CORS(app, resources={
    r"/api/*": {
        "origins": "*"
    }
})

# ✅ 5. REGISTER API
register_routes(app)

# ✅ 6. RUN
if __name__ == '__main__':
    print("🚀 Server jalan di http://localhost:5000")
    app.run(debug=True)