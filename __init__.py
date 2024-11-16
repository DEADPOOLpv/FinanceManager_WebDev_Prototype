from flask import Flask
from flask_cors import CORS
from .database import init_app, db, mysql
import os
from datetime import timedelta

def create_app():
    app = Flask(__name__)
    
    # Configuration

    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SESSION_PERMANENT'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Use 'None' if third-party contexts are needed
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # Session lasts for a day
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://root:G9XkVk%40%23g@localhost/Spend_smart')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'G9XkVk@#g'
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_DB'] = 'Spend_smart'

    # Initialize extensions
    CORS(app, origins="*", methods=["GET", "POST", "OPTIONS"], supports_credentials=True)
    init_app(app)

    # Register blueprints
    from .routes import main
    app.register_blueprint(main, url_prefix='/')
    return app



