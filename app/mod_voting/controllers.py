"""
Controllers for the voting module, including routes for voting functionality.
"""

from flask import (
    render_template,
    Blueprint,
    session,
    redirect,
    url_for,
    request,
    flash,
)
from app.mod_voting.models import (
    get_events_to_be_voted_for_user_id,
    get_events_by_user_id_in_voting,
    get_events_applied_for_user_id_in_voting,
    add_vote,
)

mod_voting = Blueprint("voting", __name__, url_prefix="/voting")


# Render the main voting page with events requiring the user's attention.
@mod_voting.route("/", methods=["GET", "POST"])
def main_voting():
    """
    Render the main voting page with events requiring the user's attention.
    """
    if "user_id" not in session:
        return redirect(url_for("users.log_in"))

    user_id = session.get("user_id")
    events_to_be_voted_for_user_id = get_events_to_be_voted_for_user_id(user_id)
    events_by_user_id_in_voting = get_events_by_user_id_in_voting(user_id)
    events_applied_for_user_id_in_voting = get_events_applied_for_user_id_in_voting(
        user_id
    )

    return render_template(
        "voting/main.html",
        events_to_be_voted_for_user_id=events_to_be_voted_for_user_id,
        events_by_user_id_in_voting=events_by_user_id_in_voting,
        events_applied_for_user_id_in_voting=events_applied_for_user_id_in_voting,
    )


# voting on a event
@mod_voting.route("/vote_event", methods=["GET", "POST"])
def vote_event():
    """
    Cast a vote (approve or disapprove) for a given event.
    Expects:
      - event_id (query parameter or form data)
      - vote (query parameter or form data): "true" or "false"
    """
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
        return redirect(url_for("voting.main_voting"))
    except Exception as e:
        # Handle unexpected errors
        flash("Vote recorded successfully!", "success")
        return redirect(url_for("voting.main_voting"))
