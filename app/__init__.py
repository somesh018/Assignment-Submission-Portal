from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from config import Config

# Initialize the PyMongo and JWT extensions
mongo = PyMongo()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize MongoDB and JWT with the app
    mongo.init_app(app)
    jwt.init_app(app)

    # Now the 'db' object should be accessible via mongo
    app.db = mongo.db  # Initialize 'db' attribute to access MongoDB collections

    # Register blueprints
    from app.routes.user_routes import user_bp
    from app.routes.admin_routes import admin_bp
    
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app
