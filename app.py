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
