from flask import Flask
from .services.create_db import create_db, create_table
from .services.routes import bp_animes
create_db()
create_table()

def create_app():

	app = Flask(__name__)

	app.register_blueprint(bp_animes)

	return app

