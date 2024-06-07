from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

app.config['MONGO_URI'] = 'mongodb+srv://kwabenaopokujnr:<password>@cluster0.d50csvn.mongodb.net/'  # Update with your MongoDB URI
mongo = PyMongo(app)

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

        mongo.db.users.insert_one({
            'name': name,
            'email': email,
            'password': password,
            'birthday': birthday,
            'sex': sex
        })
        
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = mongo.db.users.find_one({'email': email, 'password': password})

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

    mongo.db.reminders.insert_one({
        'reminder_type': reminder_type,
        'interval': interval
    })

    flash('Reminder set successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['contactName']
    email = request.form['contactEmail']
    message = request.form['contactMessage']

    mongo.db.contacts.insert_one({
        'name': name,
        'email': email,
        'message': message
    })

    flash('Message sent successfully!', 'success')
    return redirect(url_for('about'))

if __name__ == '__main__':
    app.run(debug=True)