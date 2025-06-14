"""
Controllers for the users module, handling routes for user authentication and management.
"""

from flask import render_template, redirect, Blueprint, url_for, session
from passlib.hash import pbkdf2_sha256
from app.mod_users.forms import LoginForm, CreateUserForm
from app.mod_users.models import add_user_to_database, get_user_id

mod_users = Blueprint("users", __name__, url_prefix="/users")

# Handle user login.
@mod_users.route("/", methods=["GET", "POST"])
def log_in():
    form = LoginForm()
    if form.validate_on_submit():
        username = form["username"].data
        user_id = get_user_id(username)
        session["user_id"] = user_id
        session["username"] = username
        return redirect(url_for("main.main"))
    return render_template("users/log_in.html", form=form)

# Handle new user registration.
@mod_users.route("/new_user", methods=["GET", "POST"])
def new_user():
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

# Handle user logout.
@mod_users.route("log_out", methods=["GET", "POST"])
def log_out():
    del session["user_id"]
    del session["username"]
    return redirect(url_for("users.log_in"))
