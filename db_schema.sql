-- table for users
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    email TEXT UNIQUE
);

-- table for events
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY, 
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    applied_for_id INT REFERENCES users(id),
    event TEXT NOT NULL,
    description TEXT,
    event_score INT,
    event_date DATE,
    voting_ended BOOLEAN NOT NULL DEFAULT FALSE,
    passed BOOLEAN NOT NULL DEFAULT FALSE
);

-- table for todos
CREATE TABLE IF NOT EXISTS todos (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    assigned_to_id INT REFERENCES users(id),
    todo TEXT NOT NULL, 
    description TEXT,
    todo_score INT,
    due_date DATE,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    verified BOOLEAN NOT NULL DEFAULT FALSE
);

-- table for votes
CREATE TABLE IF NOT EXISTS votes (
    id SERIAL PRIMARY KEY,
    event_id INT REFERENCES events(id) ON DELETE CASCADE,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    vote BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (event_id, user_id)
);

-- table for confirmed scores    
CREATE TABLE IF NOT EXISTS confirmed_score_log (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    event_id INT REFERENCES events(id) ON DELETE CASCADE,
    todo_id INT REFERENCES todos(id) ON DELETE CASCADE,
    score INT NOT NULL,
    confirmed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION check_voting_completion(v_event_id INT)
RETURNS BOOLEAN AS $$
DECLARE
    total_users INT;
    true_votes INT;
    false_votes INT;
    voting_passed BOOLEAN := FALSE; -- Default to FALSE
BEGIN
    -- Count the total number of users
    SELECT COUNT(*) INTO total_users FROM users;

    -- Count the number of "true" votes
    SELECT COUNT(*) INTO true_votes
    FROM votes
    WHERE event_id = v_event_id AND vote = TRUE;

    -- Count the number of "false" votes
    SELECT COUNT(*) INTO false_votes
    FROM votes
    WHERE event_id = v_event_id AND vote = FALSE;

    -- Check if enough votes have been cast to determine the majority
    IF true_votes >= (total_users / 2) THEN
        -- Voting can end mark as passed
        UPDATE events
        SET voting_ended = TRUE, passed = TRUE
        WHERE id = v_event_id;

        voting_passed := TRUE;

    ELSIF false_votes >= (total_users / 2) THEN
        -- Voting can end, mark as not passed
        UPDATE events
        SET voting_ended = TRUE, passed = FALSE
        WHERE id = v_event_id;

        voting_passed := FALSE;
    END IF;

    -- Return whether voting has completed
    RETURN voting_passed;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE VIEW events_and_votes_master_view AS
SELECT 
    events.id AS event_id,
    events.event,
    events.description,
    events.event_score,
    events.event_date,
    events.user_id,
    users.username,
    events.applied_for_id AS applied_for_user_id,
    applied_users.username AS applied_for_username,
    COALESCE(vote_summary.true_votes, 0) AS true_votes,
    COALESCE(vote_summary.false_votes, 0) AS false_votes,
    COALESCE(vote_summary.pending_votes, 0) AS pending_votes,
    events.voting_ended,
    events.passed
FROM events
JOIN users 
    ON events.user_id = users.id
LEFT JOIN users AS applied_users 
    ON events.applied_for_id = applied_users.id
LEFT JOIN (
    SELECT
        e.id AS event_id,
        COUNT(CASE WHEN v.vote = TRUE THEN 1 END)::INT AS true_votes,
        COUNT(CASE WHEN v.vote = FALSE THEN 1 END)::INT AS false_votes,
        (
            (SELECT COUNT(*) FROM users) - COUNT(v.vote)
        )::INT AS pending_votes
    FROM events e
    LEFT JOIN votes v
        ON v.event_id = e.id
    GROUP BY e.id
    ) AS vote_summary
ON vote_summary.event_id = events.id;