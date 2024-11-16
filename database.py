from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy

mysql = MySQL()
db = SQLAlchemy()

def insert_expense(user_id, amount, category_id, date):
    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO expenses (user_id, amount, category_id, date)
        VALUES (%s, %s, %s, %s)
    """, (user_id, amount, category_id, date))
    mysql.connection.commit()
    cursor.close()

def init_app(app):
    mysql.init_app(app)
    db.init_app(app)
