"""
Defines models and database interaction logic for the voting module.
"""

import app.db as db

def _check_voting_passed(event_id):
    # Initialize variables
    total_users = 0
    true_votes = 0
    false_votes = 0
    voting_passed = False  # Default to False

    try:
        # Count the total number of users
        sql_total_users = "SELECT COUNT(*) FROM users"
        total_users = db.query(sql_total_users)[0][0]

        # Count the number of "true" votes
        sql_true_votes = """
        SELECT COUNT(*) FROM votes
        WHERE event_id = ? AND vote = TRUE
        """
        true_votes = db.query(sql_true_votes, [event_id])[0][0]

        # Count the number of "false" votes
        sql_false_votes = """
        SELECT COUNT(*) FROM votes
        WHERE event_id = ? AND vote = FALSE
        """
        false_votes = db.query(sql_false_votes, [event_id])[0][0]

        # Check if enough votes have been cast to determine the majority
        if true_votes >= (total_users / 2):
            # Voting can end, mark as passed
            sql_update_passed = """
            UPDATE events
            SET voting_ended = TRUE, passed = TRUE
            WHERE id = ?
            """
            db.execute(sql_update_passed, [event_id])
            voting_passed = True

        elif false_votes > (total_users / 2):
            # Voting can end, mark as not passed
            sql_update_not_passed = """
            UPDATE events
            SET voting_ended = TRUE, passed = FALSE
            WHERE id = ?
            """
            db.execute(sql_update_not_passed, [event_id])
            voting_passed = False

        return voting_passed

    except Exception as e:
        print(f"Error checking voting completion: {e}")
        return None


def _update_score_log_events(event_id):
    sql = """
        WITH event_data AS (
            SELECT user_id AS created_by_user_id, applied_for_id, event_score
            FROM events
            WHERE id = ?
        )
        INSERT INTO confirmed_score_log (user_id, event_id, score, confirmed_at)
        SELECT applied_for_id, ?, event_score, CURRENT_TIMESTAMP
        FROM event_data
    """
    try:
        db.execute(sql, [event_id, event_id])
        return True
    except Exception as e:
        print(f"Error updating score log events: {e}")
        return None

# Add or update a user's vote for an event.
def add_vote(event_id, user_id, vote):
    sql = """
        INSERT INTO votes (event_id, user_id, vote)
        VALUES (?, ?, ?)
        ON CONFLICT (event_id, user_id)
        DO UPDATE SET vote = excluded.vote, created_at = CURRENT_TIMESTAMP;
    """
    try:
        db.execute(sql, [event_id, user_id, vote])

        # Check if voting is completed after adding the vote
        voting_passed = _check_voting_passed(event_id)

        if voting_passed:
            _update_score_log_events(event_id)

        return True
    except Exception as e:
        print(f"An error occurred while adding the vote: {e}")
        return None
    
# Get the events where the user has not voted yet
def get_events_to_be_voted_for_user_id(user_id):
    try:
        sql = """
            SELECT DISTINCT * 
            FROM events_and_votes_master_view
            WHERE event_id NOT IN (
                SELECT event_id FROM votes WHERE user_id = ?
            )
            AND pending_votes > 0
            AND voting_ended = FALSE
            ORDER BY pending_votes asc, event_date asc;
        """
        result = db.query(sql, [user_id])
        return result
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    
# Get events in voting
def get_all_events_in_voting():
    try:
        sql = """
            SELECT DISTINCT * 
            FROM events_and_votes_master_view
            WHERE voting_ended = FALSE
            ORDER BY pending_votes ASC, event_date ASC;
        """
        result = db.query(sql)
        return result
    except Exception as e:
        print(f"An error occurred: {e}")
        return []