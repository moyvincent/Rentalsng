from flask import Flask
from flask_migrate import Migrate
from items import items_app
from auth import auth_app, login_manager
from db import db

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

app = Flask(__name__)

app.secret_key = '12319940///sdosdcn'

# Initialize the login manager
login_manager.init_app(app)

migrate = Migrate(app, db)

# Register the routes from items.py with the main Flask app
app.register_blueprint(auth_app)
app.register_blueprint(items_app)

# Set up the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rental.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['STATIC_FOLDER'] = 'static'
db.init_app(app)

engine = create_engine('sqlite:///rental.db',
                       connect_args={'check_same_thread': False})
db.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

if __name__ == '__main__':
    app.secret_key = '12319940///sdosdcn'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
    