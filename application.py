from firebase_admin import db
from flask import Flask, flash, redirect, render_template, request, session, url_for, send_file
from flask_session import Session
from tempfile import mkdtemp
import smtplib
import pygal
import json
import numpy as np
import os
import requests
import datetime
import time
import atexit
from bokeh.embed import components
from bokeh.plotting import figure
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from helpers import apology, login_required, lookup, usd, liveUpdate, getSeries, predictHelper, allowed_file, random_ads
from sklearn import linear_model
from apscheduler.schedulers.background import BackgroundScheduler
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://vital-stack-181714.firebaseio.com/'})

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

#Configure images
UPLOAD_FOLDER = 'static/images'

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

ref = "https://vital-stack-181714.firebaseio.com/"
ref2 = db.reference("/")

@app.route("/")
@login_required
def index():
    return render_template("quote.html")
    
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        users_ref = requests.get(ref+'/users.json')
        print(users_ref.text)
        users_ref = json.loads(users_ref.text)

        if users_ref is not None:
            for users in users_ref:
                if users['username'] == request.form.get("username") and check_password_hash(users['password'], request.form.get("password")):
                    session["user_id"] = request.form.get("username")
                    return redirect(url_for("index"))
        
        return apology("Invalid Username/Password", 400)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        if not request.form.get("email"):
            return apology("must provide email id", 400)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password and confirmation match
        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        # hash the password and insert a new user in the database
        hash = generate_password_hash(request.form.get("password"))
        users_ref = requests.get(ref+'/users.json')
        user_count = requests.get(ref+'/user_count.json').text
        print(users_ref.text)
        users_ref = json.loads(users_ref.text)
        print(user_count)
        # unique username constraint violated?
        if users_ref is not None:
            for users in users_ref:
                if users['username'] == request.form.get("username"):
                    return apology("username taken", 400)

        ref2.child('users').child(user_count).set({
                'username': request.form.get("username"),
                'email': request.form.get("email"),
                'password': hash
        })

        user_count = int(user_count) + 1
        ref2.update({'user_count': user_count})
        session["user_id"] = request.form.get("username")
        # Display a flash message
        flash("Registered!")
        # Redirect user to home page
        return redirect(url_for("index"))
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

#run cron jobs
scheduler = BackgroundScheduler()
scheduler.start()