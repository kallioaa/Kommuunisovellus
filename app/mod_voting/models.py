"""
Defines models and database interaction logic for the voting module.
"""

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app import db

# check if voting has completed using an sql function
def _check_vote_passed(event_id):
    sql = "SELECT check_voting_completion(:event_id)"
    try:
        result = db.session.execute(text(sql), {"event_id": int(event_id)}).scalar()
        return result
    except SQLAlchemyError as e:
        print(f"An error occurred while checking if voting has ended: {e}")
        return None



def _update_score_log_events(event_id):
    sql = """
        WITH event_data AS (
            SELECT user_id AS created_by_user_id, applied_for_id, event_score
            FROM events
            WHERE id = :event_id
        )
        INSERT INTO confirmed_score_log (user_id, event_id, score, confirmed_at)
        SELECT applied_for_id, :event_id, event_score, CURRENT_TIMESTAMP
        FROM event_data
        """
    try:
        db.session.execute(text(sql), {"event_id": event_id})
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()

# Add or update a user's vote for an event.
def add_vote(event_id, user_id, vote):
    sql = """
        INSERT INTO votes (event_id, user_id, vote)
        VALUES (:event_id, :user_id, :vote)
        ON CONFLICT (event_id, user_id)
        DO UPDATE SET vote = EXCLUDED.vote, created_at = CURRENT_TIMESTAMP;
        """
    try:
        with db.session.begin():
            db.session.execute(
                text(sql), {"event_id": event_id, "user_id": user_id, "vote": vote}
            )
            voting_completed = _check_vote_passed(event_id)
            if voting_completed is None:
                raise RuntimeError("Voting completion check failed. Rolling back.")
            if voting_completed:
                _update_score_log_events(event_id)
        return "Vote successfully added or updated."
    except RuntimeError as e:
        db.session.rollback()
        return f"An error occurred while adding the vote: {e}"


# get the events where the user has not voted yet
def get_events_to_be_voted_for_user_id(user_id):
    try:
        # Use the SQL function to get events and filter for those the user has not voted
        sql = """
            SELECT DISTINCT * 
            FROM events_and_votes_master_view
            WHERE event_id NOT IN (
                SELECT event_id FROM votes WHERE user_id = :user_id
            )
            AND pending_votes > 0
            AND voting_ended = FALSE;
        """
        result = db.session.execute(text(sql), {"user_id": int(user_id)})
        return result.fetchall()
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        return []

# get the events created by the user which are currently in voting
def get_events_by_user_id_in_voting(user_id):
    try:
        # Use the SQL function to get events and filter for those created by the user
        sql = """
            SELECT DISTINCT * 
            FROM events_and_votes_master_view
            WHERE user_id = :user_id
            AND voting_ended = FALSE;
        """
        result = db.session.execute(text(sql), {"user_id": user_id})
        return result.fetchall()
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        return []

# get the voting situation for events applied for the user
def get_events_applied_for_user_id_in_voting(user_id):
    try:
        # Use the SQL function to get events and filter for those applied for the user
        sql = """
            SELECT DISTINCT * 
            FROM events_and_votes_master_view
            WHERE applied_for_user_id = :user_id
            AND voting_ended = FALSE;
        """
        result = db.session.execute(text(sql), {"user_id": user_id})
        return result.fetchall()
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        return []
