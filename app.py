from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate # type: ignore
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure random secret key

# Configure SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'healthyou.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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

@app.route('/')
def index():
    return render_template('index.html')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_verify = request.form['passwordVerify']
        birthday = request.form['birthday']
        sex = request.form['sex']

        if not all([name, username, email, password, password_verify, birthday, sex]):
            return jsonify({"message": "Missing data"}), 400

        if password != password_verify:
            return jsonify({"message": "Passwords do not match!"}), 400

        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
        if existing_user:
            return jsonify({"message": "Email or Username already exists!"}), 400

        new_user = User(name=name, username=username, email=email, birthday=birthday, sex=sex)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id
        return jsonify({"message": "Account created successfully!"}), 200

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        login_identity = data.get('login_identity')
        password = data.get('password')

        if not login_identity or not password:
            return jsonify({"message": "Missing data"}), 400

        user = User.query.filter((User.email == login_identity) | (User.username == login_identity)).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            return jsonify({"message": "Login successful!", "redirect_url": url_for('features')}), 200
        else:
            return jsonify({"message": "Invalid credentials!"}), 401

    return render_template('login.html')

@app.route('/features', methods=['GET', 'POST'])
@login_required
def features():
    if request.method == 'POST':
        reminder_type = request.form.get('reminder-type')
        interval = request.form.get('interval')
        new_reminder = Reminder(user_id=session['user_id'], reminder_type=reminder_type, interval=interval)
        db.session.add(new_reminder)
        db.session.commit()
        return redirect(url_for('features'))
    
    return render_template('features.html')

@app.route('/get_reminders')
def get_reminders():
    if 'user_id' not in session:
        return jsonify([])

    reminders = Reminder.query.filter_by(user_id=session['user_id']).all()
    return jsonify([{
        'id': reminder.id,
        'reminder_type': reminder.reminder_type,
        'interval': reminder.interval
    } for reminder in reminders])

@app.route('/set_reminder', methods=['POST'])
def set_reminder():
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    reminder_type = request.form.get('reminder-type')
    interval = request.form.get('interval')

    if not reminder_type or not interval:
        return jsonify({"message": "Missing data"}), 400

    new_reminder = Reminder(user_id=session['user_id'], reminder_type=reminder_type, interval=interval)
    db.session.add(new_reminder)
    db.session.commit()
    return jsonify({"message": "Reminder set successfully"}), 200

@app.route('/complete_reminder/<int:reminder_id>', methods=['POST'])
def complete_reminder(reminder_id):
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    reminder = Reminder.query.get(reminder_id)
    if reminder and reminder.user_id == session['user_id']:
        reminder.completed = True
        db.session.commit()
        return jsonify({"message": "Reminder marked as completed"}), 200

    return jsonify({"message": "Reminder not found"}), 404

@app.route('/delete_reminder/<int:reminder_id>', methods=['DELETE'])
def delete_reminder(reminder_id):
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    reminder = Reminder.query.get(reminder_id)
    if reminder and reminder.user_id == session['user_id']:
        db.session.delete(reminder)
        db.session.commit()
        return jsonify({"message": "Reminder deleted successfully"}), 200
    return jsonify({"message": "Reminder not found"}), 404

@app.route('/about')
@login_required
def about():
    return render_template('about.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logged out successfully!"}), 200

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['contactName']
    email = request.form['contactEmail']
    message = request.form['contactMessage']

    new_contact = Contact(name=name, email=email, message=message)
    db.session.add(new_contact)
    db.session.commit()

    return jsonify({"message": "Message sent successfully!"}), 200

if __name__ == '__main__':
    db.create_all()  # Create tables if they don't exist
    app.run(debug=True)