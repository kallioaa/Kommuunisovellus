-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- table for users
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    email TEXT UNIQUE
);

-- table for events
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    applied_for_id INTEGER REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    event TEXT NOT NULL,
    description TEXT,
    event_score INTEGER NOT NULL,
    event_date DATE NOT NULL,
    voting_ended INTEGER NOT NULL DEFAULT 0,
    passed INTEGER NOT NULL DEFAULT 0
);

-- table for todos
CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    assigned_to_id INTEGER REFERENCES users(id),
    todo TEXT NOT NULL, 
    description TEXT,
    todo_score INTEGER,
    due_date DATE,
    completed INTEGER NOT NULL DEFAULT 0,
    verified INTEGER NOT NULL DEFAULT 0
);

-- table for votes
CREATE TABLE IF NOT EXISTS votes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER REFERENCES events(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    vote INTEGER NOT NULL, -- 0 for False, 1 for True
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (event_id, user_id)
);

-- table for confirmed scores    
CREATE TABLE IF NOT EXISTS confirmed_score_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    event_id INTEGER REFERENCES events(id) ON DELETE CASCADE,
    todo_id INTEGER REFERENCES todos(id) ON DELETE CASCADE,
    score INTEGER NOT NULL,
    confirmed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


DROP VIEW IF EXISTS events_and_votes_master_view;

CREATE VIEW events_and_votes_master_view AS
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
        COUNT(CASE WHEN v.vote = TRUE THEN 1 END) AS true_votes,
        COUNT(CASE WHEN v.vote = FALSE THEN 1 END) AS false_votes,
        (
            (SELECT COUNT(*) FROM users) - COUNT(v.vote)
        ) AS pending_votes
    FROM events e
    LEFT JOIN votes v
        ON v.event_id = e.id
    GROUP BY e.id
) AS vote_summary
ON vote_summary.event_id = events.id;