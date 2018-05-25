from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

# create application
def create_app():

    app = Flask(__name__)

    # Initializing flask extensions
    db.init_app(app)
    login_manager.init_app(app)