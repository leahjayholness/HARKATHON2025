from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_apscheduler import APScheduler

db = SQLAlchemy()
migrate = Migrate()
scheduler = APScheduler()

def create_app(config_class="config.Config"):
    """Application factory to create and configure the Flask app."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    global bcrypt
    bcrypt = Bcrypt(app)

    # Initialize extensions
    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)
        scheduler.init_app(app)

    scheduler.start()
    
    # Register blueprints
    from app.controllers import register_controllers
    register_controllers(app)

    return app