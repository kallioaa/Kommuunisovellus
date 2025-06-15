"""
Controllers for the users module, handling routes for user authentication and management.
"""

from flask import render_template, redirect, Blueprint, url_for, session, request, flash
from werkzeug.security import generate_password_hash
import secrets
from app.mod_users.models import add_user_to_database, get_user_id
from app.mod_users.models import check_login_authorized, username_exists, email_exists

mod_users = Blueprint("users", __name__, url_prefix="/users")

# Handle user login.
@mod_users.route("/", methods=["GET", "POST"])
def log_in():
    if request.method == "GET":
        return render_template("users/log_in.html")

    if request.method == "POST":
        form = request.form
        username = form["username"]
        password = form["password"]

        # Check if the user exists and the password is correct
        if not username or not password:
            flash("Username and password are required.", "danger")
            return render_template("users/log_in.html")
    
        if not check_login_authorized(username, password):
            flash("Invalid username or password.", "danger")
            return render_template("users/log_in.html")

        # If login is successful, set session variables
        user_id = get_user_id(username)
        session["csrf_token"] = secrets.token_hex(16)  # Generate a CSRF token
        session["user_id"] = user_id
        session["username"] = username
        return redirect(url_for("main.main"))


# Handle new user registration.
@mod_users.route("/new_user", methods=["GET", "POST"])  
def new_user():
    if request.method == "GET":
        return render_template("users/new_user.html")
    
    if request.method == "POST":
        form = request.form
        username = form["username"]
        password = form["password"]
        password_repeat = form["password_repeat"]
        email = form["email"]

        # Check if all fields are filled
        if not username or not password or not password_repeat or not email:
            flash("All fields are required.", "danger")
            return render_template("users/new_user.html")

        # Check if passwords match
        if password != password_repeat:
            flash("Passwords do not match.", "danger")
            return render_template("users/new_user.html")
        
        # check if username already exists
        if username_exists(username):
            flash("Username already exists.", "danger")
            return render_template("users/new_user.html")
        
        # check if email already exists
        if email_exists(email):
            flash("Email already exists.", "danger")
            return render_template("users/new_user.html")
        
        # Hash the password
        password_hashed = generate_password_hash(password)

        # Add the user to the database
        if add_user_to_database(username, password_hashed, email):
            flash("User created successfully!", "success")
            return redirect(url_for("users.log_in"))
        else:
            flash("Failed to create user. Please try again.", "danger")
            return render_template("users/new_user.html")



# Handle user logout.
@mod_users.route("log_out", methods=["GET", "POST"])
def log_out():
    del session["user_id"]
    del session["username"]
    return redirect(url_for("users.log_in"))
