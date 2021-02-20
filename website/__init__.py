from os import path

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = 'my_database.db'

"""
Create our flask app and initialize secret key.
"""


def create_app():
    app = Flask(__name__)
    # secure cookies and session data related to our website.
    app.config['SECRET_KEY'] = 'josh secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # integrate db w/ app.
    db.init_app(app)

    from .views import views
    from .auth import auth

    # '/' indicates no prefix. for these routes after root page. we just register our route files here as we go.
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    """
    Used to load information w/ a user, i.e., query the DB for this user and get user entity by primary key (id)
    """

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database successfully!')
