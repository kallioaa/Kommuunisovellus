"""
This module initializes the Flask application, sets configurations, 
registers blueprints, and handles errors for the application.
"""

from os import getenv
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

# Initialize the Flask application
app = Flask(__name__)

# Application configurations
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = getenv("SQLALCHEMY_TRACK_MODIFICATIONS")

# Initialize the SQLAlchemy instance
db = SQLAlchemy()
db.init_app(app)

# Initialize Flask-Bootstrap
Bootstrap(app)


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


# Blueprint imports
from app.mod_users.controllers import mod_users  # noqa: E402
from app.mod_main.controllers import mod_main  # noqa: E402
from app.mod_events.controllers import mod_events  # noqa: E402
from app.mod_voting.controllers import mod_voting  # noqa: E402
from app.mod_todos.controllers import mod_todos  # noqa: E402

# Register blueprints
app.register_blueprint(mod_users)
app.register_blueprint(mod_main)
app.register_blueprint(mod_events)
app.register_blueprint(mod_voting)
app.register_blueprint(mod_todos)
