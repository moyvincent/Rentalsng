from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import ForeignKey, create_engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

# Models should come in here
class User(db.Model, UserMixin):
    __tablename__ = 'users' # specify the table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    # One-to-Many relationship between User and Rentals
    item = relationship('Item', backref='user', lazy=True)

# class Vendor(db.Model, UserMixin):
#     __tablename__ = 'vendors' # specify the table name
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     email = db.Column(db.String(50), unique=True, nullable=False)
#     address = db.Column(db.String(200), nullable=False)
#     password = db.Column(db.String(255), nullable=False)
#     phone_number = db.Column(db.String(20), nullable=False)
#     is_admin = db.Column(db.Boolean, default=False)
#     is_active = db.Column(db.Boolean, default=True)
#     is_vendor = db.Column(db.Boolean, default=True)
#     company_name = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.String(500), nullable=False)
#     registration_date = db.Column(db.DateTime, default=datetime.utcnow)

#     # Relationships
#     items = relationship('Item', backref='vendor', lazy=True)

class Item(db.Model):
    __tablename__ = 'items'  # specify the table name
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(255), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)

    # One-to-Many relationship between Rental and Booking
    booking = relationship('Booking', backref='item', lazy=True)

class Booking(db.Model):
    __tablename__ = 'bookings'  # specify the table name
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, ForeignKey('items.id'), nullable=False)

    # One-to-Many relationship between Booking and User
    user = relationship('User', backref='booking', lazy=True)

engine = create_engine('sqlite:///rental.db')
db.metadata.create_all(bind=engine)