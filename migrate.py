from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, init, migrate, upgrade
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')  # Use environment variable for security
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import will be models here
from app import User, Reminder, Contact

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Adjust length to handle hashed password
    birthday = db.Column(db.String(10), nullable=False)
    sex = db.Column(db.String(10), nullable=False)

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reminder_type = db.Column(db.String(100), nullable=False)
    interval = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(500), nullable=False)

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