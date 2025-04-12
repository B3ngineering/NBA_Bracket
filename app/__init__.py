from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    # Register blueprints
    from app.routes.api import api
    from app.routes.web import web
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(web)

    return app
