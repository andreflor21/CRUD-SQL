from flask import Flask
from .controllers.create_db import create_db, create_table

create_db()
create_table()

app = Flask(__name__)


@app.route('/')
def index():
	return "Hello World"
