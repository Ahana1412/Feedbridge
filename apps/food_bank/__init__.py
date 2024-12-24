from flask import Blueprint

blueprint = Blueprint('food_bank_blueprint', __name__, url_prefix='/food_bank')

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'your-database-uri-here'
    db.init_app(app)
    return app
