from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__) # __name__ represents the name of the file ran
    app.config['SECRET_KEY'] = 'sjahdkjahsjdkh sakhdkjash' # encrypt the cookies and session data
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    # url_prefix means: for ex. on views file when you define a route like 'xyz', when you want to access it you need to write "/url_prefix/xyz", so we just leave the prefix / like this.

    from .models import User, Note
    # create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.signin'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# def create_database(app):
#     if not path.exists('website/' + DB_NAME):
#         with app.app_context():
#             db.create_all()
#         print("Created")
