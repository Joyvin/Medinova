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
    my_name = db.Column(db.String(150))
    image_file = db.Column(db.String(50))
    image_data = db.Column(db.LargeBinary)
    image_mimetype = db.Column(db.Text, nullable=False)
    pdf_file = db.Column(db.String(50))
    pdf_data = db.Column(db.LargeBinary)
    pdf_mimetype = db.Column(db.Text, nullable=False)
    emer_name = db.Column(db.String(150))
    emer_phone = db.Column(db.String(150))
    emer_email = db.Column(db.String(150))
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))