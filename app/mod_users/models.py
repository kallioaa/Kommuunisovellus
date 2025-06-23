from werkzeug.security import check_password_hash
import app.db as db

# Check if a username exists in the database.
def username_exists(username):
    try:
        sql = "SELECT COUNT(*) FROM users WHERE username = ?"
        result = db.query(sql, [username])
        count = result[0][0] if result else 0
        return bool(count)
    except Exception as e:
        print(f"Error checking username existence: {e}")
        return None

def email_exists(email):
    try:
        sql = "SELECT COUNT(*) FROM users WHERE email = ?"
        result = db.query(sql, [email])
        count = result[0][0] if result else 0
        return bool(count)
    except Exception as e:
        print(f"Error checking email existence: {e}")
        return None

def add_user_to_database(username, password_hashed, email):
    try:
        sql = "INSERT INTO users (username, password, email) VALUES (?, ?, ?)"
        db.execute(sql, [username, password_hashed, email])
        return True
    except Exception as e:
        print(f"Error inserting user: {e}")
        return None

def check_login_authorized(username, password):
    try:
        sql = "SELECT password FROM users WHERE username = ?"
        result = db.query(sql, [username])
        if not result:
            return False
        password_hashed_from_db = result[0][0]
        correct = check_password_hash(password_hashed_from_db, password)
        return correct
    except Exception as e:
        print(f"Error checking login authorization: {e}")
        return None

def get_user_id(username):
    try:
        sql = "SELECT id FROM users WHERE username = ?"
        result = db.query(sql, [username])
        user_id = result[0][0] if result else None
        return user_id
    except Exception as e:
        print(f"Error getting user ID: {e}")
        return None

def get_usernames_and_emails():
    try:
        sql = "SELECT id, username, email FROM users"
        result = db.query(sql)
        return result
    except Exception as e:
        print(f"Error getting usernames and emails: {e}")
        return None