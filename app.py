from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure MongoDB
app.config["MONGO_URI"] = "mongodb+srv://kwabenaopokujnr:479NLxEglkWkDSd4@cluster0.d50csvn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = mongo.db.users.find_one({"email": email})

        if user and check_password_hash(user['password'], password):
            session['user'] = user['name']
            session['email'] = user['email']
            return redirect(url_for('features'))
        else:
            return 'Invalid email or password'
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        mongo.db.users.insert_one({
            "name": name,
            "email": email,
            "password": hashed_password
        })

        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/account')
def account():
    if 'user' in session:
        return render_template('account.html', user=session['user'])
    return redirect(url_for('login'))

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/set_reminder', methods=['POST'])
def set_reminder():
    if 'email' not in session:
        return redirect(url_for('login'))

    reminder_type = request.form['reminder-type']
    interval = request.form['interval']

    reminder = {
        "email": session['email'],
        "reminder_type": reminder_type,
        "interval": interval
    }

    mongo.db.reminders.insert_one(reminder)
    return redirect(url_for('features'))

@app.route('/get_reminders')
def get_reminders():
    if 'email' not in session:
        return jsonify([])

    reminders = list(mongo.db.reminders.find({"email": session['email']}))
    for reminder in reminders:
        reminder['_id'] = str(reminder['_id'])

    return jsonify(reminders)

@app.route('/delete_reminder/<reminder_id>', methods=['DELETE'])
def delete_reminder(reminder_id):
    if 'email' not in session:
        return jsonify({"status": "not authorized"}), 403

    mongo.db.reminders.delete_one({"_id": ObjectId(reminder_id)})
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(debug=True)