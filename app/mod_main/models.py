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
        raise e

