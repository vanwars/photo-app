from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import random

'''
References:
    * https://dev.to/kaelscion/authentication-hashing-in-sqlalchemy-1bem
'''
from . import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password_plaintext = db.Column(db.String(128), nullable=False) #terrible idea...just for debugging
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    image_url = db.Column(db.String(300), nullable=True)
    thumb_url = db.Column(db.String(300), nullable=True)
    date_created = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    is_verified = db.Column(db.Boolean(), nullable=False, default=False)
    is_disabled = db.Column(db.Boolean(), nullable=False, default=False)
    
    def __init__(self, first_name:str, last_name:str, username:str, email:str, 
            image_url:str=None, thumb_url:str=None):

        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.image_url = image_url
        self.thumb_url = thumb_url

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self): 
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
            'image_url': self.image_url,
            'thumb_url': self.thumb_url
        }         

