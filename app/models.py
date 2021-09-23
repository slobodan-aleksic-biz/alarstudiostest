from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from init import app


bcrypt = Bcrypt()

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(1024), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, name, username, password, is_admin):
        self.name = name
        self.username = username
        self.password = password
        self.is_admin = is_admin
