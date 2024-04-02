import sqlite3
import datetime

from flask import redirect, render_template, session, flash
from datetime import datetime as dt
from functools import wraps


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            flash('Please login to access this page','warning')
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def is_email_in_database(email):
    # Connect to the SQLite database (replace 'your_database.db' with your actual database file)
    connection = sqlite3.connect('website_data.db')
    cursor = connection.cursor()

    # Execute a query to check if the email exists in the 'users' table
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))

    # Fetch the result
    result = cursor.fetchone()

    # Close the database connection
    connection.close()

    # Return True if the email exists, False otherwise
    return bool(result)


def get_time():
    """Returns formatted local time."""

    return dt.now().strftime("%Y-%m-%d %H:%M:%S")

