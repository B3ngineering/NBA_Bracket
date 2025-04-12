from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
# from app.models.models import User

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # User loader function
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.models import User
        return User.query.get(int(user_id))  # Assuming User is your user model

    # Register blueprints
    from app.routes.api import api
    from app.routes.web import web
    from app.auth.auth import auth
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(web)
    app.register_blueprint(auth)

    return app