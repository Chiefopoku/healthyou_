from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, init, migrate, upgrade
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure random secret key

# Configure SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'healthyou.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    birthday = db.Column(db.String(10), nullable=False)
    sex = db.Column(db.String(10), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

# Define Reminder model
class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reminder_type = db.Column(db.String(100), nullable=False)
    interval = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)

# Define Contact model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(500), nullable=False)

# Ensure migrations folder exists
migrate_directory = os.path.join(os.path.dirname(__file__), 'migrations')
if not os.path.exists(migrate_directory):
    os.makedirs(migrate_directory)

# Use the application context for migration commands
with app.app_context():
    if not os.path.exists(os.path.join(migrate_directory, 'alembic.ini')):
        init(directory=migrate_directory)
    migrate(message="Initial migration.", directory=migrate_directory)
    upgrade(directory=migrate_directory)