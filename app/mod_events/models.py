"""
Models for handling event-related database operations in the mod_events module.
"""
import app.db as db 

# Function to add an event to the database
def add_event_to_database(event_data):
    try:
        sql = """
            INSERT INTO events (user_id, applied_for_id, event, description, event_score, event_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        db.execute(
            sql,
            [
                event_data["user_id"],
                event_data["applied_for_id"],
                event_data["event"],
                event_data["description"],
                event_data["event_score"],
                event_data["event_date"],
            ],
        )

        new_event_id = db.last_insert_id()
        return new_event_id

    except Exception as e:
        print(f"Error inserting event: {e}")
        return None

# Function to retrieve all passed events
def get_all_passed_events():
    try:
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

        rows = db.query(sql)
        events = [dict(row) for row in rows]  # Convert sqlite3.Row to dict
        return events

    except Exception as e:
        print(f"Error retrieving passed events: {e}")
        return []

# delete event
def delete_event(event_id):
    try:
        sql = """
            DELETE FROM events
            WHERE id = ?
        """
        db.execute(sql, [event_id])
        return True

    except Exception as e:
        print(f"Error deleting event: {e}")
        return None