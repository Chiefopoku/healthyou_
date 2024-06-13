from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, init, migrate, upgrade
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Emmanue1.@localhost/healthyou'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import your models here
from app import User, Reminder, Contact

def run_migrations():
    with app.app_context():
        try:
            init()
        except Exception as e:
            print(f"Init exception: {e}")
        migrate(message="Initial migration.")
        upgrade()

if __name__ == '__main__':
    run_migrations()