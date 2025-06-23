"""
Defines the main blueprint and routes for the application's main page.
"""

from flask import render_template, Blueprint, session, redirect, url_for
from app.mod_user_summary.models import get_commune_credit_scores_summary, get_total_score, get_todo_summary, get_event_summary

mod_user_summary = Blueprint("mod_user_summary", __name__, url_prefix="/")

# function for rendering the main page
@mod_user_summary.route("/", methods=["GET", "POST"])
def main():
    if "user_id" not in session:
        return redirect(url_for("users.log_in"))
    
    # get user id and username from session
    user_id = session.get("user_id")
    username = session.get("username")

    # table with credit scores summary
    commune_credit_scores_summary = get_commune_credit_scores_summary()
    entries_score_summary = [
        {"user_id": entry["user_id"], "username": entry["username"], "score": entry["total_score"]} for entry in commune_credit_scores_summary
    ]
    # Sort: highest score first, then alphabetical username
    entries_score_summary.sort(key=lambda x: (-x["score"], x["username"]))

    # get total score for the user
    total_score = get_total_score(user_id)

    # get event summary
    event_summary = get_event_summary(user_id)

    # get todo summary
    todo_summary = get_todo_summary(user_id)

    
    return render_template("user_summary/main.html", 
                           entries_score_summary=entries_score_summary,
                           user_id=user_id,
                           username=username,
                           total_score=total_score,
                           event_summary=event_summary,
                           todo_summary=todo_summary
    )
