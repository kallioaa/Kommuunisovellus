import app.db as db # Assuming db.py is in the same directory

# Function to retrieve all todos from the database
def get_all_todos():
    try:
        sql = """
        SELECT 
            t.id AS todo_id,
            t.user_id AS user_id,
            a.id AS assigned_to_id,
            u.username AS username,
            a.username AS assigned_to_username,
            t.todo, 
            t.description, 
            t.todo_score, 
            t.due_date,
            t.completed,
            t.verified
        FROM todos t
            JOIN users u ON t.user_id = u.id
        LEFT JOIN users a ON t.assigned_to_id = a.id
        ORDER BY t.due_date DESC
        """
        rows = db.query(sql)

        # Convert each row to a dict
        todos = [dict(row) for row in rows]
        return todos
    except Exception as e:
        print(f"Error retrieving todos: {e}")
        return None

# Insert a new todo into the database and return its primary key.
def add_todo_to_database(user_id, todo, description, todo_score, due_date):
    try:
        sql = """
            INSERT INTO todos (user_id, todo, description, todo_score, due_date)
            VALUES (?, ?, ?, ?, ?)
        """
        db.execute(
            sql,
            [user_id, todo, description, todo_score, due_date],
        )
        new_todo_id = db.last_insert_id()
        return new_todo_id

    except Exception as e:
        print(f"Error inserting todo: {e}")
        return None

# Function to assign a todo to a user.
def assign_todo_to_user(todo_id, user_id):
    try:
        sql = """
            UPDATE todos
            SET assigned_to_id = ?
            WHERE id = ?
        """
        db.execute(sql, [user_id, todo_id])
    except Exception as e:
        print(f"Error assigning todo: {e}")
        raise e

# Mark an existing todo as completed in the database.
def complete_todo_in_database(todo_id):
    try:
        sql = """
            UPDATE todos
            SET completed = TRUE
            WHERE id = ?
        """
        db.execute(sql, [todo_id])
    except Exception as e:
        print(f"Error completing todo: {e}")
        raise e

# Mark an existing todo as verified in the database and update the score log accordingly.
def verify_todo_in_database(todo_id):
    try:
        # Mark the todo as verified
        sql = """
            UPDATE todos
            SET verified = TRUE
            WHERE id = ?
        """
        db.execute(sql, [todo_id])

        # Update the score log
        _update_score_log_todo(todo_id)

    except Exception as e:
        print(f"Error verifying todo: {e}")
        raise e
    
# drop todo from database if it has not been assigned to anyone or completed.
def drop_todo_from_database(todo_id):
    try:
        sql = """
            DELETE FROM todos
            WHERE id = ? AND assigned_to_id IS NULL AND completed = FALSE
        """
        db.execute(sql, [todo_id])
    except Exception as e:
        print(f"Error deleting todo: {e}")
        raise e

# Update the 'confirmed_score_log' table based on a verified todo's information.
def _update_score_log_todo(todo_id):
    sql = """
    WITH todo_data AS (
        SELECT user_id AS created_by_user_id, assigned_to_id, todo_score
        FROM todos
        WHERE id = ?
    )
    INSERT INTO confirmed_score_log (user_id, todo_id, score, confirmed_at)
    SELECT assigned_to_id, ?, todo_score, CURRENT_TIMESTAMP
    FROM todo_data
    UNION ALL
    SELECT created_by_user_id, ?, -todo_score, CURRENT_TIMESTAMP
    FROM todo_data;
    """
    try:
        db.execute(sql, [todo_id, todo_id, todo_id])
    except Exception as e:
        print(f"Error updating score log: {e}")
        raise e