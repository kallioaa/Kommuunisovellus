"""
This module initializes the Flask application, sets configurations, 
registers blueprints, and handles errors for the application.
"""
from os import getenv
from flask import Flask

# Initialize the Flask application
app = Flask(__name__)

# initialize the app configuration
app.secret_key = getenv("SECRET_KEY")

# Blueprint imports
from app.mod_users.controllers import mod_users  # noqa: E402
from app.mod_main.controllers import mod_main  # noqa: E402
from app.mod_events.controllers import mod_events  # noqa: E402
from app.mod_todos.controllers import mod_todos  # noqa: E402
from app.mod_voting.controllers import mod_voting  # noqa: E402

# Register blueprintss
app.register_blueprint(mod_users)
app.register_blueprint(mod_main)
app.register_blueprint(mod_events)
app.register_blueprint(mod_todos)
app.register_blueprint(mod_voting)
