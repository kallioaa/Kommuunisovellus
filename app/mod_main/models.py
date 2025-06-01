from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app import db


# get scores from the databases for all the users
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
        result = db.session.execute(text(sql))
        rows = result.fetchall()
        # Convert each row (SQLAlchemy Row object) into a dict
        scores = [row._mapping for row in rows]
        return scores
    except SQLAlchemyError as e:
        print(f"Error retrieving credit scores summary: {e}")
        raise e
