"""
Defines the main blueprint and routes for the application's main page.
"""

from flask import render_template, Blueprint, session, redirect, url_for
from app.mod_main.models import get_commune_credit_scores_summary

mod_main = Blueprint("main", __name__, url_prefix="/")

# function for rendering the main page
@mod_main.route("/", methods=["GET", "POST"])
def main():
    if "user_id" not in session:
        return redirect(url_for("users.log_in"))

    commune_credit_scores_summary = get_commune_credit_scores_summary()
    
    # entries to the main page
    entries = [
        {"username": entry["username"], "score": entry["total_score"]} for entry in commune_credit_scores_summary
    ]

    # Sort: highest score first, then alphabetical username
    entries.sort(key=lambda x: (-x["score"], x["username"]))
    
    return render_template("main/main.html", entries=entries)
