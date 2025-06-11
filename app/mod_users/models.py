from passlib.hash import pbkdf2_sha256
import app.db as db

# Check if a username exists in the database.
def username_exists(username):
    sql = "SELECT COUNT(*) FROM users WHERE username = ?"
    result = db.query(sql, [username])
    count = result[0][0] if result else 0
    return bool(count)

def email_exists(email):
    sql = "SELECT COUNT(*) FROM users WHERE email = ?"
    result = db.query(sql, [email])
    count = result[0][0] if result else 0
    return bool(count)

def add_user_to_database(username, password_hashed, email):
    try:
        sql = "INSERT INTO users (username, password, email) VALUES (?, ?, ?)"
        db.execute(sql, [username, password_hashed, email])
        return True
    except Exception as e:
        print(f"Error inserting user: {e}")
        return False

def check_login_authorized(username, password):
    sql = "SELECT password FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return False
    password_hashed_from_db = result[0][0]
    correct = pbkdf2_sha256.verify(password, password_hashed_from_db)
    return correct

def get_user_id(username):
    sql = "SELECT id FROM users WHERE username = ?"
    result = db.query(sql, [username])
    user_id = result[0][0] if result else None
    return user_id

def get_usernames_and_emails():
    sql = "SELECT username, email FROM users"
    result = db.query(sql)
    return result