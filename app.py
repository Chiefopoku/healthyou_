from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthyou.db'
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

        new_user = User(name=name, email=email, password=password, birthday=birthday, sex=sex)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email, password=password).first()

        if user:
            flash('Login successful!', 'success')
            return redirect(url_for('account'))
        else:
            flash('Invalid credentials!', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/set_reminder', methods=['POST'])
def set_reminder():
    reminder_type = request.form['reminder-type']
    interval = request.form['interval']

    new_reminder = Reminder(reminder_type=reminder_type, interval=interval)
    db.session.add(new_reminder)
    db.session.commit()

    flash('Reminder set successfully!', 'success')
    return redirect(url_for('index'))

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
    db.create_all()  # Create tables if they don't exist
    app.run(debug=True)