from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
from models import db, User, Reminder, Progress
from config import Config
from datetime import datetime
import jwt
import os

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
mail = Mail(app)
scheduler = BackgroundScheduler()

# Secret key for JWT
app.config['SECRET_KEY'] = 'your_secret_key'

# User registration with email confirmation
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    new_user = User(email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    
    # Send confirmation email
    token = jwt.encode({'email': data['email']}, app.config['SECRET_KEY'], algorithm='HS256')
    confirmation_url = f"http://localhost:5000/confirm_email/{token}"
    msg = Message('Email Confirmation', sender='your_email@gmail.com', recipients=[data['email']])
 # msg = Message('Email Confirmation', sender='your_email@gmail.com', recipients=[data['email']])    msg.body = f'Please confirm your email by clicking on the link: {confirmation_url}'
    mail.send(msg)

 #     return jsonify({'message': 'User registered successfully! Please check your email to confirm.'}), 201

@app.route('/confirm_email/<token>', methods=['GET'])
def confirm_email(token):
    try:
        email = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['email']
        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify({'message': 'Email confirmed!'}), 200
        return jsonify({'message': 'User not found!'}), 404
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expired!'}), 400
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token!'}), 400

@app.route('/set_reminder', methods=['POST'])
def set_reminder():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user:
        new_reminder = Reminder(time=data['time'], user=user)
        db.session.add(new_reminder)
        db.session.commit()
        return jsonify({'message': 'Reminder set successfully!'}), 201
    return jsonify({'message': 'User not found!'}), 404

@app.route('/view_reminders/<email>', methods=['GET'])
def view_reminders(email):
    user = User.query.filter_by(email=email).first()
    if user:
        reminders = Reminder.query.filter_by(user_id=user.id).all()
        return jsonify([{'id': r.id, 'time': r.time} for r in reminders]), 200
    return jsonify({'message': 'User not found!'}), 404

@app.route('/delete_reminder/<int:reminder_id>', methods=['DELETE'])
def delete_reminder(reminder_id):
    reminder = Reminder.query.get(reminder_id)
    if reminder:
        db.session.delete(reminder)
        db.session.commit()
        return jsonify({'message': 'Reminder deleted successfully!'}), 200
    return jsonify({'message': 'Reminder not found!'}), 404

@app.route('/update_reminder/<int:reminder_id>', methods=['PUT'])
