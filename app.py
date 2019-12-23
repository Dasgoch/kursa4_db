from flask import Flask
from config import Configuration
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Configuration)
app.config['SECRET_KEY'] = 'you-will-never-guess'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
