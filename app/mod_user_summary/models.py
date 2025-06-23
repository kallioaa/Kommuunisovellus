import app.db as db

# Get scores from the databases for all the users
def get_commune_credit_scores_summary():
    sql = """
    SELECT
        u.id AS user_id,
        u.username,
        COALESCE(SUM(csl.score), 0) AS total_score
    FROM users u
    LEFT JOIN confirmed_score_log csl ON csl.user_id = u.id
    GROUP BY u.id, u.username
    ORDER BY total_score DESC;
    """
    try:
        rows = db.query(sql)
        # Convert each row to a dict
        scores = [dict(row) for row in rows]
        return scores
    except Exception as e:
        print(f"Error retrieving credit scores summary: {e}")
        return []

# get total score for the user
def get_total_score(user_id):
    sql_total_score = """
        SELECT COALESCE(SUM(score), 0) AS total_score
        FROM confirmed_score_log
        WHERE user_id = ?;
    """
    try:
        rows = db.query(sql_total_score, [user_id])
        total_score = rows[0][0]
        return total_score
    except Exception as e:
        print(f"Error retrieving total score: {e}")
        return None
    

# event summary
def get_event_summary(user_id):
    sql_event_summary = """
        SELECT 
            u.id AS user_id,
            u.username,

            -- Number of confirmed events assigned to the user
            (
                SELECT COUNT(*)
                FROM events
                WHERE applied_for_id = u.id AND voting_ended = 1 AND passed = 1
            ) AS confirmed_events_assigned_to_user,

            -- Number of events created by the user
            (
                SELECT COUNT(*)
                FROM events
                WHERE user_id = u.id
            ) AS events_created_by_user,

            -- Total score from confirmed events
            (
                SELECT COALESCE(SUM(score), 0)
                FROM confirmed_score_log
                WHERE user_id = u.id AND event_id IS NOT NULL
            ) AS total_confirmed_event_score

        FROM users u
        WHERE u.id = ?;
    """
    try:
        rows = db.query(sql_event_summary, [user_id])
        event_summary = dict(rows[0])
        return event_summary
    except Exception as e:
        print(f"Error retrieving event summary: {e}")
        return {}


# get todo summart
def get_todo_summary(user_id):
    sql_todo_summary = """
        SELECT 
            u.id AS user_id,
            u.username,
            
            -- Number of completed todos assigned to the user
            (
                SELECT COUNT(*)
                FROM todos
                WHERE assigned_to_id = u.id AND completed = 1
            ) AS completed_todos_assigned_to_user,

            -- Number of todos created by the user
            (
                SELECT COUNT(*)
                FROM todos
                WHERE user_id = u.id
            ) AS todos_created_by_user,

            -- Total score from confirmed todos
            (
                SELECT COALESCE(SUM(score), 0)
                FROM confirmed_score_log
                WHERE user_id = u.id AND todo_id IS NOT NULL
            ) AS total_confirmed_todo_score

        FROM users u
        WHERE u.id = ?;

    """
    try:
        rows = db.query(sql_todo_summary, [user_id])
        todo_summary = dict(rows[0])
        return todo_summary
    except Exception as e:
        print(f"Error retrieving completed todos count: {e}")
        return {}

