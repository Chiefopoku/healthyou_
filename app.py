from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
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
            flash('Passwords do not match!', 'error')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password, birthday=birthday, sex=sex)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully!', 'success')
        return redirect(url_for('features'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            flash('Login successful!', 'success')
            return redirect(url_for('features'))
        else:
            flash('Invalid credentials!', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/account')
def account():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('account.html', user=session['user_name'])

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/set_reminder', methods=['POST'])
def set_reminder():
    if 'user_id' not in session:
        return jsonify({"status": "not authorized"}), 403

    reminder_type = request.form['reminder-type']
    interval = request.form['interval']

    new_reminder = Reminder(reminder_type=reminder_type, interval=interval, user_id=session['user_id'])
    db.session.add(new_reminder)
    db.session.commit()

    flash('Reminder set successfully!', 'success')
    return redirect(url_for('features'))

@app.route('/get_reminders')
def get_reminders():
    if 'user_id' not in session:
        return jsonify([])

    reminders = Reminder.query.filter_by(user_id=session['user_id']).all()
    reminders_list = [{"id": r.id, "reminder_type": r.reminder_type, "interval": r.interval} for r in reminders]
    return jsonify(reminders_list)

@app.route('/delete_reminder/<int:reminder_id>', methods=['DELETE'])
def delete_reminder(reminder_id):
    if 'user_id' not in session:
        return jsonify({"status": "not authorized"}), 403

    reminder = Reminder.query.filter_by(id=reminder_id, user_id=session['user_id']).first()
    if reminder:
        db.session.delete(reminder)
        db.session.commit()
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "not found"}), 404

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['contactName']
    email = request.form['contactEmail']
    message = request.form['contactMessage']

    new_contact = Contact(name=name, email=email, message=message)
    db.session.add(new_contact)
    db.session.commit()

    flash('Message sent successfully!', 'success')
    return redirect(url_for('about'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)