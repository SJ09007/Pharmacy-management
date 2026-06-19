from flask import Flask
import os
from flask_session import Session
from .database import init_db

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'pharmacy-dev-key')
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['UPLOAD_FOLDER'] = 'uploads/prescriptions'
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB

    Session(app)
    init_db()

    from .routes.auth import auth_bp
    from .routes.inventory import inventory_bp
    from .routes.customers import customers_bp
    from .routes.billing import billing_bp
    from .routes.prescriptions import prescriptions_bp
    from .routes.dashboard import dashboard_bp
    from .routes.ocr import ocr_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(billing_bp)
    app.register_blueprint(prescriptions_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(ocr_bp)

    return app
