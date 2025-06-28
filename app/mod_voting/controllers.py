"""
Controllers for the voting module, including routes for voting functionality.
"""

from flask import (
    Blueprint,
    session,
    redirect,
    url_for,
    request,
    flash,
)
from app.mod_voting.models import (
    add_vote,
)

mod_voting = Blueprint("voting", __name__, url_prefix="/voting")


# voting on a event
@mod_voting.route("/vote_event", methods=["GET", "POST"])
def vote_event():
    if "user_id" not in session:
        return redirect(url_for("users.log_in"))

    # Extract the event_id from request args or form
    event_id = request.args.get("event_id")

    # Get the vote from request args or form
    vote_str = request.args.get("vote") or request.form.get("vote")

    # Convert vote from string to boolean
    vote_str_lower = vote_str.lower()
    vote_bool = vote_str_lower == "true"

    # Get the current user's ID from the session
    user_id = session.get("user_id")

    try:
        # Use the add_vote function to record the vote (True = approve, False = disapprove)
        add_vote(event_id=event_id, user_id=user_id, vote=vote_bool)
        flash("Vote recorded successfully!", "success")
        return redirect(url_for("user_summary.main"))
    except Exception as e:
        # Handle unexpected errors
        flash("Vote recording failed. Please try again.", "danger")
        return redirect(url_for("user_summary.main"))