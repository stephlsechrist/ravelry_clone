# from crypt import methods
from hashlib import new
from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

# below is how to create flask route/endpoint
@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password): # pass in hashed pw from DB and then password typed in by user to check 
                flash('Logged in!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect!', category='error')
        else:
            flash('User does not exist!', category='error')
                
    return render_template("login.html", user=current_user)

@auth.route("/sign-up", methods=['GET', 'POST'] )
def sign_up():
    if request.method == 'POST':
        email = request.form.get("email") # access info via name attribute, not id
        # username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        # looking in User model to see if email typed in matches one in model
        email_exists = User.query.filter_by(email=email).first()
        # username_exists = User.query.filter_by(username=username).first()
        
        if email_exists:
            flash('Email is already in use.', category='error') # messages on screen
        # elif username_exists:
        #     flash('Username is already in use.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        # elif len(username) < 2:
        #     flash('Username is too short', category='error')
        elif len(password1) < 6:
            flash('Password is too short.', category='error')
        elif len(email) < 4:
            flash('Email is invalid.', category='error')
        else:
            new_user = User(email=email, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user) # adds to staging area before going into db
            db.session.commit() # commits to DB
            login_user(new_user, remember=True)
            flash('User created!')
            return redirect(url_for('views.home'))
            
    return render_template("signup.html", user=current_user)

# login_required decorator makes it so that you can't get to this route without being logged in first
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))