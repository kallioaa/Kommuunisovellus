"""
Controllers for the events module, handling routes for creating and managing events.
"""

from flask import render_template, Blueprint, session, redirect, url_for, flash, request
from app.mod_events.models import add_event_to_database, get_all_passed_events
from app.mod_users.models import get_usernames_and_emails, get_user_id
from app.mod_voting.models import add_vote

mod_events = Blueprint("events", __name__, url_prefix="/events")

# function for rendering the main events page
@mod_events.route("/", methods=["GET", "POST"])
def main():
    if "user_id" not in session:
        return redirect(url_for("users.log_in"))
    all_events = get_all_passed_events()

    return render_template("events/main.html", all_events=all_events)

# function for creating a new event
@mod_events.route("/new_event", methods=["GET", "POST"])
def new_event():
    if "user_id" not in session:
        return redirect(url_for("users.log_in"))
    
    # Populate the dropdown with usernames and emails
    result = get_usernames_and_emails()
    choices = [(row["username"], f"{row['username']} ({row['email']})") for row in result]

    

    if request.method == "GET":
        return render_template("events/new_event.html", applying_event_choices=choices)
    
    if request.method == "POST":
        # check csrf token
        form = request.form
        if form["csrf_token"] != session["csrf_token"]:
            flash("Invalid CSRF token.", "danger")
            return redirect(url_for("users.log_in"))

        # Get form data and validate
        user_id = session.get("user_id")
        applying_for_username = form["applying_event_for"]
        applying_for_id = get_user_id(applying_for_username)
        event = form["event"]
        description = form["description"]
        event_score = form["event_score"]
        event_date = form["event_date"]
        if not applying_for_username or not event or not event_score or not event_date:
            flash("Some required fields are not filled.", "danger")
            return render_template("events/new_event.html", applying_event_choices=choices)

        event_dict = {
            "user_id": user_id,
            "applied_for_id": applying_for_id,
            "event": event,
            "description": description,
            "event_score": event_score,
            "event_date": event_date,
        }
        # Add the event to the database
        event_id = add_event_to_database(event_dict)
        if event_id:
            # Add an approving vote for the event
            vote_added = add_vote(user_id=user_id, event_id=event_id, vote=True)
            if not vote_added:
                flash("Failed to add vote.", "danger")
                return render_template("events/new_event.html", applying_event_choices=choices)
            
            flash("Event created and vote added successfully!", "success")
            return redirect(url_for("events.main"))
        flash("Failed to create event.", "danger")
        return render_template("events/new_event.html", applying_event_choices=choices)
