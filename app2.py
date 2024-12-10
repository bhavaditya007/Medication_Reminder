from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medication_reminder.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Reminder model
class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    reminder_time = db.Column(db.DateTime, nullable=False)

# Initialize the database with application context
def init_db():
    with app.app_context():  # Ensure this runs inside the app context
        db.create_all()

# Registration route (POST)
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')

    # Check if the user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "Email already exists!"}), 400  # Bad Request if email already exists
    
    # Create new user and add to the database
    new_user = User(email=email, phone=phone, password=password)
    
    db.session.add(new_user)
    db.session.commit()
    
    print("Error")

    return jsonify({"message": "User registered successfully!", "user_id": new_user.id}), 201  # Created

# Login route (POST)
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email, password=password).first()

    if user:
        return jsonify({"message": "Login successful", "user_id": user.id})
    else:
        return jsonify({"message": "Invalid credentials"}), 401  # Unauthorized if credentials are incorrect

# Home page route
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reminders', methods=['POST'])
def create_reminder():
    try:
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        reminder_time = data.get('reminder_time')

        # Validate input
        if not title or not description or not reminder_time:
            return jsonify({"message": "All fields are required!"}), 400

        # Convert reminder_time to datetime
        reminder_time = datetime.fromisoformat(reminder_time)

        # Create and save the reminder
        new_reminder = Reminder(
            title=title,
            description=description,
            reminder_time=reminder_time
        )
        db.session.add(new_reminder)
        db.session.commit()

        return jsonify({"message": "Reminder created successfully!", "reminder_id": new_reminder.id}), 201
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "An error occurred while creating the reminder."}), 500


if __name__ == '__main__':
    # Initialize the database here
    init_db()
    app.run(debug=True)