# /config.py
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'G9XkVk@#g'
MYSQL_DB = 'Spend_smart'
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
SQLALCHEMY_TRACK_MODIFICATIONS = False 