"""
Models for handling event-related database operations in the mod_events module.
"""

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app import db

# Function to add an event to the database
def add_event_to_database(event_data):
    try:
        sql = """
            INSERT INTO events (user_id, applied_for_id, event, description, event_score, event_date)
            VALUES (:user_id, :applied_for_id, :event, :description, :event_score, :event_date)
            RETURNING id
        """

        result = db.session.execute(
            text(sql),
            {
                "user_id": event_data["user_id"],
                "applied_for_id": event_data["applied_for_id"],
                "event": event_data["event"],
                "description": event_data["description"],
                "event_score": event_data["event_score"],
                "event_date": event_data["event_date"],
            },
        )

        db.session.commit()

        new_event_id = result.fetchone()[0]
        return new_event_id

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error inserting event: {e}")
        return None

# Function to retrieve all passed events
def get_all_passed_events():
    sql = """
    SELECT 
        e.id AS event_id,
        e.user_id AS user_id,
        u.username AS username, 
        a.username AS applied_for_username, 
        e.event, 
        e.description, 
        e.event_score, 
        e.event_date
    FROM events e
    JOIN users u ON e.user_id = u.id
    LEFT JOIN users a ON e.applied_for_id = a.id
    WHERE e.voting_ended = TRUE 
      AND e.passed = TRUE
    """

    result = db.session.execute(text(sql))
    rows = result.fetchall()

    events = [row._mapping for row in rows]
    return events

# delete event
def delete_event(event_id):
    try:
        sql = """
            DELETE FROM events
            WHERE id = :event_id
        """
        db.session.execute(text(sql), {"event_id": event_id})
        db.session.commit()
        return True

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error deleting event: {e}")
        return False
