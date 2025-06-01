"""
Models for the users module, providing functions for user management such as 
authentication, user creation, and data retrieval.
"""

from passlib.hash import pbkdf2_sha256
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app import db

# Check if a username exists in the database.
def username_exists(username):
    sql = "SELECT COUNT(*) FROM users WHERE username = :username"
    r = db.session.execute(text(sql), {"username": username})
    count = r.first()[0]
    return bool(count)


def email_exists(email):
    sql = "SELECT COUNT(*) FROM users WHERE email = :email"
    r = db.session.execute(text(sql), {"email": email})
    count = r.first()[0]
    return bool(count)


def add_user_to_database(username, password_hashed, email):
    try:
        sql = "INSERT INTO users (username, password, email) values (:username, :password, :email)"
        db.session.execute(
            text(sql),
            {"username": username, "password": password_hashed, "email": email},
        )
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error inserting user: {e}")
        return False


def check_login_authorized(username, password):
    sql = "SELECT password FROM users WHERE username = :username"
    r = db.session.execute(text(sql), {"username": username})
    r_first = r.first()
    if r_first is None:
        return False
    password_hashed_from_db = r_first[0]
    correct = pbkdf2_sha256.verify(password, password_hashed_from_db)
    return correct


def get_user_id(username):
    sql = "SELECT id FROM users WHERE username = :username"
    r = db.session.execute(text(sql), {"username": username})
    user_id = r.first()[0]
    return user_id


def get_usernames_and_emails():
    sql = "SELECT username, email FROM users"
    result = db.session.execute(text(sql))
    return result
