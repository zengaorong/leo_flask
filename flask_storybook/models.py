# models.py
from .ext import db

#创建ORM模型类
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    addresses = db.relationship('Address', backref='user')

    def __init__(self, username):
        self.username = username


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, email_address):
        self.email_address = email_address