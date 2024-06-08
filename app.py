from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

# Configure SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'healthyou.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    birthday = db.Column(db.String(10), nullable=False)
    sex = db.Column(db.String(10), nullable=False)

# Define Reminder model
class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reminder_type = db.Column(db.String(100), nullable=False)
    interval = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Define Contact model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/features')
def features():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('features.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        password_verify = request.form['passwordVerify']
        birthday = request.form['birthday']
        sex = request.form['sex']

        if password != password_verify:
            return jsonify({"message": "Passwords do not match!"}), 400

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"message": "Email already exists!"}), 400

        new_user = User(name=name, email=email, password=password, birthday=birthday, sex=sex)
        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id
        return jsonify({"message": "Account created successfully!"}), 200

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email, password=password).first()

        if user:
            session['user_id'] = user.id
            return jsonify({"message": "Login successful!"}), 200
        else:
            return jsonify({"message": "Invalid credentials!"}), 401

    return render_template('login.html')

@app.route('/account')
def account():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('account.html', user=user)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/set_reminder', methods=['POST'])
def set_reminder():
    if 'user_id' not in session:
        return jsonify({"message": "Please log in to set a reminder"}), 403

    reminder_type = request.form['reminder-type']
    interval = request.form['interval']
    user_id = session['user_id']

    new_reminder = Reminder(reminder_type=reminder_type, interval=interval, user_id=user_id)
    db.session.add(new_reminder)
    db.session.commit()

    return jsonify({"message": "Reminder set successfully!"}), 200

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['contactName']
    email = request.form['contactEmail']
    message = request.form['contactMessage']

    new_contact = Contact(name=name, email=email, message=message)
    db.session.add(new_contact)
    db.session.commit()

    return jsonify({"message": "Message sent successfully!"}), 200

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

@app.route('/delete_reminder/<int:reminder_id>', methods=['DELETE'])
def delete_reminder(reminder_id):
    if 'user_id' not in session:
        return jsonify({"message": "Not authorized"}), 403

    reminder = Reminder.query.get(reminder_id)
    if reminder:
        db.session.delete(reminder)
        db.session.commit()
        return jsonify({"message": "Reminder deleted successfully!"}), 200
    else:
        return jsonify({"message": "Reminder not found"}), 404

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logged out successfully!"}), 200

if __name__ == '__main__':
    db.create_all()  # Create tables if they don't exist
    app.run(debug=True)