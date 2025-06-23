"""
Defines the main blueprint and routes for the application's main page.
"""

from flask import render_template, Blueprint, session, redirect, url_for, request
from app.mod_user_summary.models import get_commune_credit_scores_summary, get_total_score, get_todo_summary, get_event_summary
from app.mod_users.models import get_usernames_and_emails

mod_user_summary = Blueprint("user_summary", __name__, url_prefix="/")

# function for rendering the main page
@mod_user_summary.route("/", methods=["GET", "POST"])
def main():
    if "user_id" not in session:
        return redirect(url_for("users.log_in"))
    
    # take user_id and username from request arguments if available
    user_id = request.args.get("user_id")
    username = request.args.get("username")

    if user_id is None or username is None:
        # if not provided, get from session
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
                           user_id=int(user_id),
                           username=username,
                           total_score=total_score,
                           event_summary=event_summary,
                           todo_summary=todo_summary
    )

# user search functionality
@mod_user_summary.route("/user_search", methods=["GET", "POST"])
def user_search():
    if "user_id" not in session:
        return redirect(url_for("users.log_in"))
    
    # Get the search query from the request arguments
    search_query = request.args.get("search_query", "").strip()
    
    # Fetch usernames and emails based on the search query
    results = get_usernames_and_emails()

    # filter results based on the search query
    if search_query:
        results = [row for row in results if search_query.lower() in row["username"].lower() or search_query.lower() in row["email"].lower()]
    
    return render_template("user_summary/user_search.html", results=results, search_query=search_query)
