# define database modules here
from enum import unique
from time import timezone
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# a model is a table
# in this case, a row is a User and every column is data about that user
class User(db.Model, UserMixin):
    # define columns (at least one must be primary key)
    id = db.Column(db.Integer, primary_key=True) # will automatically give unique ID
    email = db.Column(db.String(150), unique=True) # strings must have max length defined
    # username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    # yarns=db.relationship('Yarn', backref='user', passive_deletes=True)
    # needles=db.relationship('Needle', backref='user', passive_deletes=True)
    
class Yarn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(40), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    weight = db.Column(db.String(20), nullable=False)
    material = db.Column(db.String(40), nullable=True)
    amount = db.Column(db.Integer, nullable=True)
    date_added = db.Column(db.DateTime(timezone=True), default=func.now())
    date_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    
class Needle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gauge = db.Column(db.Integer, nullable=False)
    length = db.Column(db.Integer, nullable=True)
    type = db.Column(db.String(20), nullable=False)    
    date_added = db.Column(db.DateTime(timezone=True), default=func.now())
    date_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
   