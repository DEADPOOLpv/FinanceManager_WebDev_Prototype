from .database import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'  
    user_id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Expenses(db.Model):
    __tablename__ = 'expenses'  
    expense_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)  
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False, default=db.func.current_date())
    salary = db.Column(db.Float, nullable=False, default=0.00)

class CategoryExpenses(db.Model):
    __tablename__ = 'categories'
    category_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    category_name = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)


