from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)
app.app_context().push()

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)

class Expenses(db.Model):
        id = db.Column(db.Integer(), primary_key = True)
        owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
        date = db.Column(db.Date())
        exp_name = db.Column(db.String())
        amount = db.Column(db.Integer())
        paymode = db.Column(db.String())
        category = db.Column(db.String())
db.create_all()



