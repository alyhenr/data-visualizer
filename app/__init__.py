from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'app/uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max size

    # Register the blueprint
    from .routes import routes_bp
    app.register_blueprint(routes_bp)

    return app
