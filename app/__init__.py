from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


login_manager = LoginManager()
db = SQLAlchemy()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////var/db/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
login_manager.init_app(app)

from app.routes import *
from app.models import *
from app.forms import *
#app.app_context().push()
#db.create_all()

#def create_app():
#    app = Flask(__name__)
#    db.init_app(app)
#    return app