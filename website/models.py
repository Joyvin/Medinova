from . import db
from flask_login import UserMixin
import datetime

class User(db.Model, UserMixin): # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    person = db.Column(db.String(150))
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    uploads = db.relationship('Upload')

class Upload(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    # pdf_file = db.Column(db.LargeBinary)
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))