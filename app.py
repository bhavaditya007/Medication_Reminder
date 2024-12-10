from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medication_reminder.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Reminder model
class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    medication = db.Column(db.String(100), nullable=False)
    reminder_time = db.Column(db.String(50), nullable=False)  # Store time as a string (e.g., '2024-12-09 09:00:00')
    sound = db.Column(db.String(50), nullable=False)
    user = db.relationship('User', backref=db.backref('reminders', lazy=True))

# Initialize the database
def create_tables():
    with app.app_context():
        db.create_all()

create_tables()

# Home page route
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email, password=password).first()
    if user:
        return jsonify({"success": True, "user_id": user.id})
    else:
        return jsonify({"success": False}), 401


# Set reminder route
@app.route('/set-reminder', methods=['POST'])
def set_reminder():
    data = request.get_json()
    medication = data.get('medication')
    reminder_time = data.get('reminderTime')
    sound = data.get('sound')
    user_id = data.get('user_id')  # User ID from frontend

    # Create and store the reminder
    reminder = Reminder(medication=medication, reminder_time=reminder_time, sound=sound, user_id=user_id)
    db.session.add(reminder)
    db.session.commit()

    return jsonify({"message": "Reminder set successfully!"})

# Get reminders route
@app.route('/get-reminders', methods=['GET'])
def get_reminders():
    user_id = request.args.get('user_id')  # User ID from query params
    reminders = Reminder.query.filter_by(user_id=user_id).all()
    reminders_list = [{"medication": r.medication, "reminder_time": r.reminder_time, "sound": r.sound} for r in reminders]
    return jsonify(reminders_list)

if __name__ == '__main__':
    app.run(debug=True)
