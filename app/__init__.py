# app/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()  # loads .env

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object('app.config.Config')

    db.init_app(app)

    # Import and register routes
    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    # start scheduler
    from app.tasks import start_scheduler
    start_scheduler(app)

    return app

# For running with `python -m app`
if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
