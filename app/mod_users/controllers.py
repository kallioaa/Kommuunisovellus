"""
Controllers for the users module, handling routes for user authentication and management.
"""

from flask import render_template, redirect, Blueprint, url_for, session
from passlib.hash import pbkdf2_sha256
from app.mod_users.forms import LoginForm, CreateUserForm
from app.mod_users.models import add_user_to_database, get_user_id

mod_users = Blueprint("users", __name__, url_prefix="/users")


@mod_users.route("/", methods=["GET", "POST"])
def log_in():
    """
    Handle user login.

    - Displays the login form.
    - Authenticates the user and sets session variables if login is successful.

    Returns:
        - Redirects to the main page on successful login.
        - Renders the login page if validation fails.
    """
    form = LoginForm()
    if form.validate_on_submit():
        username = form["username"].data
        user_id = get_user_id(username)
        session["user_id"] = user_id
        session["username"] = username
        return redirect(url_for("main.main"))
    return render_template("users/log_in.html", form=form)


@mod_users.route("/new_user", methods=["GET", "POST"])
def new_user():
    """
    Handle new user registration.

    - Displays the registration form.
    - Hashes the password and adds the user to the database if the form is valid.

    Returns:
        - Redirects to the login page on successful registration.
        - Renders the registration page if validation fails.
    """
    form = CreateUserForm()
    if form.validate_on_submit():
        print("testis")
        username = form["username"].data
        password = form["password"].data
        password_hashed = pbkdf2_sha256.hash(password)
        email = form["email"].data
        add_user_to_database(username, password_hashed, email)
        return redirect(url_for("users.log_in"))
    return render_template("users/new_user.html", form=form)


@mod_users.route("log_out", methods=["GET", "POST"])
def log_out():
    """
    Handle user logout.

    - Removes session variables associated with the user.
    - Redirects to the login page.

    Returns:
        Redirect to the login page.
    """
    session.pop("user_id", None)
    return redirect(url_for("users.log_in"))
