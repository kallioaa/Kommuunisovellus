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

    # add the vote
    success = add_vote(event_id=event_id, user_id=user_id, vote=vote_bool)

    if not success:
        flash("Failed to record vote. Please try again.", "danger")
        return redirect(url_for("user_summary.main"))
    
    # If the vote was successfully recorded, redirect to the user summary page
    flash("Vote recorded successfully!", "success")
    return redirect(url_for("user_summary.main"))
