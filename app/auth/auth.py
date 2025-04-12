from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user
from app.models.models import User
from app import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Fetch the user from the database
        user = User.query.filter_by(username=username).first()
        
        if user and user.verify_password(password):  # Assuming you have a method to verify passwords
            login_user(user)  # Log the user in
            return redirect(url_for('web.index'))  # Redirect to the homepage
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if the username or email already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists. Please choose another.', 'danger')
            return redirect(url_for('auth.register'))

        # Create a new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)  # Hash the password
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')