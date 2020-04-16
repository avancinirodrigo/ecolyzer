from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()
bp = Blueprint('', __name__)

def create_app(config=Config):
	app = Flask(__name__)
	app.config.from_object(config)	
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app)

	from . import routes
	app.register_blueprint(bp)

	return app
