import os
import re
import sqlite3
import calendar

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import is_email_in_database, login_required, get_time

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# SQLite Database Initialization
conn = sqlite3.connect('website_data.db')
db = conn.cursor()
db.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        telephone TEXT NOT NULL,
        date_of_birth TEXT NOT NULL,
        date_of_account_creation TEXT NOT NULL
    )
''')

db.execute('''
    CREATE TABLE IF NOT EXISTS reservations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        procedure TEXT NOT NULL,
        comment TEXT NOT NULL,
        date_of_appointment TEXT NOT NULL,
        date_of_reserving TEXT NOT NULL
    )
''')

conn = sqlite3.connect('website_data.db')
db = conn.cursor()

conn.commit()
# conn.close()

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        conn = sqlite3.connect('website_data.db')
        db = conn.cursor()

        email = request.form.get("email")
        password = request.form.get("password")

        if any(not entry for entry in [email,password]):
            return render_template("login.html", message = "Fields cannot be empty!")

        conn = sqlite3.connect('website_data.db')
        db = conn.cursor()
        db.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = db.fetchone()

        if user:

            # Ensure username exists and password is correct
            if not check_password_hash(user[4], request.form.get("password")):
                flash('Invalid password', 'error')
                return render_template("login.html")
            flash('Successfuly logged in', 'success')
            # Remember which user has logged in
            session["user_id"] = user[0]

            # Redirect user to home page

            return redirect("/")

        else:
            flash('No account with this email', 'error')
    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("login.html", message = "again")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    flash('Logged out successful', 'success')

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Retrieve form data
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmPassword")
        telephone = request.form.get("telephone")
        date_of_birth = request.form.get("date_of_birth")

        conn = sqlite3.connect('website_data.db')
        db = conn.cursor()

        # Check if any field is empty
        if not all([first_name, last_name, email, password, confirm_password, telephone, date_of_birth]):
            flash('Please fill in all fields', 'error')
            return redirect("register")

        # Check if password and confirm password match
        if password != confirm_password:
            flash('Password and Confirm Password do not match', 'error')
            return redirect("register")

        if len(password) < 8:
            flash('Password must be at least 8 characters long', 'error')
            return redirect("register")

        if is_email_in_database(email):
            flash('Email already used', 'error')
            return redirect("register")

        if len(telephone) != 11:
            flash('Incomplete mobile number', 'error')
            return redirect("register")

        # Save data to the database
        hashed_password = generate_password_hash(password)
        db.execute('''
            INSERT INTO users (first_name, last_name, email, password, telephone, date_of_birth, date_of_account_creation)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, email, hashed_password, telephone, date_of_birth, get_time()))

        db.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = db.fetchone()
        session["user_id"] = user[0]

        conn.commit()
        # conn.close()

        flash('Registration successful!', 'success')
        return redirect("/")
    return render_template("register.html")


@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == 'POST':
        email = request.form.get("email")
        new_password = request.form.get("password")
        confirm_password = request.form.get("confirmPassword")

        if not all([email, new_password, confirm_password]):
            flash('Please fill in all fields', 'error')
            return redirect("forgot")

        if len(new_password) < 8:
            flash('Password must be at least 8 characters long', 'error')
            return redirect("forgot")

        # Check if the email exists in the database
        conn = sqlite3.connect('website_data.db')
        db = conn.cursor()
        db.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = db.fetchone()

        if user:
            # Check if new password and confirmation match
            if new_password != confirm_password:
                flash('Passwords do not match', 'error')
                return redirect("forgot")

            # Update password in the database
            hashed_password = generate_password_hash(new_password)

            conn = sqlite3.connect('website_data.db')
            db = conn.cursor()
            db.execute('UPDATE users SET password = ? WHERE email = ?', (hashed_password, email))
            conn.commit()
            # conn.close()

            flash('Password reset successfully', 'success')
            return redirect("login")
        else:
            flash('Email not found in the database', 'error')

    return render_template('forgot.html')



@app.route("/reserve", methods=["GET", "POST"])
@login_required
def reserve():
    # Sample list of procedures
    procedures = ["Crowns", "Braces", "Teeth Whitening"]

    if request.method == "POST":

        # Retrieve form data
        procedure = request.form.get("procedure")
        comment = request.form.get("comment")
        date_of_appointment = request.form.get("date_of_appointment")

        conn = sqlite3.connect('website_data.db')
        db = conn.cursor()

        # Check if any field is empty
        if not all([procedure, date_of_appointment]):
            flash('Please fill in all fields', 'error')
            return render_template("reserve.html", procedures=procedures)

        db.execute('SELECT date_of_appointment FROM reservations WHERE date_of_appointment = ?', (date_of_appointment,))
        date_available = db.fetchone()
        if date_available:
            flash('This timing is reserved', 'error')
            return render_template("reserve.html", procedures=procedures)

        if not check_cancellation(date_of_appointment):
            flash('Date already passed', 'error')
            return render_template("reserve.html", procedures=procedures)

        if not all([comment]):
            comment = "Empty"

        db.execute('''
            INSERT INTO reservations (user_id, procedure, comment, date_of_appointment, date_of_reserving)
            VALUES (?, ?, ?, ?, ?)
        ''', (session["user_id"], procedure, comment, date_of_appointment, get_time()))

        conn.commit()
        # conn.close()

        flash('Reservation successful!', 'success')
        return redirect("/")
    return render_template("reserve.html", procedures=procedures)


@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    conn = sqlite3.connect('website_data.db')
    db = conn.cursor()

    user_id = session["user_id"]
    db.execute("SELECT * FROM reservations WHERE user_id = ?", (user_id,))
    no_appointment = db.fetchone()

    if not no_appointment:
        flash('You have no bookings', 'warning')
        return render_template("history.html", no_booking="none")

    reservations = db.execute("SELECT id, procedure, comment, date_of_appointment FROM reservations WHERE user_id = ?", (user_id,))

    if request.method == "POST":
        selected_button = str(request.form.get("selected_button"))

        db.execute('SELECT * FROM reservations WHERE date_of_appointment = ?', (selected_button,))
        date = db.fetchone()

        db.execute("DELETE FROM reservations WHERE user_id = ? AND date_of_appointment = ?", (user_id, selected_button,))
        conn.commit()
        flash('Cancelled Reservation','success')
        return redirect("/history")

    # conn.commit()
    # conn.close()

    return render_template("history.html", reservations=reservations)


@app.route("/admin", methods=["GET", "POST"])
# @login_required
def admin():
    if 'user_id' in session:
        if session["user_id"] == 2:
            return render_template("admin.html")
    return redirect("/")


@app.route("/info_general")
def info_general():
   return render_template("info_general.html")


@app.route("/info_cosmetic")
def info_cosmetic():
   return render_template("info_cosmetic.html")


@app.route("/info_surgical")
def info_surgical():
   return render_template("info_surgical.html")


def check_cancellation(date):
    now = get_time()
    if date[2:4] > now[2:4]:
        return True
    elif date[2:4] == now[2:4]:
        if date[5:7] > now[5:7]:
            return True
        elif date[5:7] == now[5:7]:
            if date[8:10] >= now[8:10]:
                return True
    return False
app.jinja_env.globals.update(check_cancellation=check_cancellation)
