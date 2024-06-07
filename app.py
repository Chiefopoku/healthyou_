from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure MongoDB
app.config["MONGO_URI"] = "mongodb+srv://kwabenaopokujnr:479NLxEglkWkDSd4@cluster0.d50csvn.mongodb.net/"
mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user = mongo.db.users.find_one({"email": email})

        if user and check_password_hash(user['password'], password):
            session['user'] = user['name']
            session['email'] = user['email']
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "failure", "message": "Invalid email or password"}), 401
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.form
        name = data['name']
        email = data['email']
        password = data['password']
        hashed_password = generate_password_hash(password)

        if mongo.db.users.find_one({"email": email}):
            return jsonify({"status": "failure", "message": "Email already exists"}), 400

        mongo.db.users.insert_one({
            "name": name,
            "email": email,
            "password": hashed_password
        })

        return jsonify({"status": "success"}), 200
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
    return jsonify({"status": "success"}), 200

@app.route('/set_reminder', methods=['POST'])
def set_reminder():
    if 'email' not in session:
        return jsonify({"status": "not authorized"}), 403

    data = request.form
    reminder_type = data['reminder-type']
    interval = data['interval']

    reminder = {
        "email": session['email'],
        "reminder_type": reminder_type,
        "interval": interval
    }

    mongo.db.reminders.insert_one(reminder)
    return jsonify({"status": "success"}), 200

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