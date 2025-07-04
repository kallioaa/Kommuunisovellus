-- Insert example Finnish profile names with hashed passwords
INSERT INTO users (username, password, email) VALUES
('Matti', 'pbkdf2_sha256$260000$randomsalt1$hashedpassword1', 'matti@example.com'),
('Liisa', 'pbkdf2_sha256$260000$randomsalt2$hashedpassword2', 'liisa@example.com'),
('Pekka', 'pbkdf2_sha256$260000$randomsalt3$hashedpassword3', 'pekka@example.com'),
('Sanna', 'pbkdf2_sha256$260000$randomsalt4$hashedpassword4', 'sanna@example.com'),
('Jukka', 'pbkdf2_sha256$260000$randomsalt5$hashedpassword5', 'jukka@example.com'),
('Testaaja', 'scrypt:32768:8:1$xenzQUmicAZvOTmC$5e71784d9dce867a817b7fb2992d394662191bdbcb71f5a3d2e550259555be8064dd9da19ef1f763bd79049d8f602403d9a5010a22ff1291e34877a7052d5454', 'testaaja@gmail.com');

-- Insert example events
INSERT INTO events (id, user_id, applied_for_id, event, description, event_score, event_date, voting_ended, passed) VALUES
(1, 1, 2, 'Ei vetänyt vessaa', 'Taaskaan...', -85, '2023-11-01', FALSE, FALSE),
(2, 3, 4, 'Järjesti Kirjakerhon tapaamisen', 'Kirjakerhon kuukausittainen tapaaminen', 90, '2023-11-05', FALSE, TRUE),
(3, 5, 1, 'Ei tiskannut kattilaa', 'siivotonta...', -75, '2023-11-10', FALSE, FALSE),
(4, 2, 3, 'Ulkoilutti koiran', 'Lenkki Julosaaren ympäristössä', 80, '2023-11-15', FALSE, TRUE),
(5, 4, 5, 'Rikkoi television', 'tiputti telkkarin seinältä. Kustannukset suuret', -95, '2023-11-20', FALSE, FALSE);

-- Insert example todos
INSERT INTO todos (user_id, assigned_to_id, todo, description, todo_score, due_date, completed, verified) VALUES
(1, 2, 'Siivous', 'Siivoa yhteiset tilat', 50, '2023-11-25', TRUE, TRUE),
(3, 4, 'Kirjojen järjestäminen', 'Järjestä kirjat aakkosjärjestykseen', 30, '2023-11-30', FALSE, FALSE),
(6, 1, 'Joogamattojen puhdistus', 'Puhdista joogamatot tunnin jälkeen', 20, '2023-12-01', TRUE, TRUE),
(2, 3, 'Ruoanlaittovälineiden tarkistus', 'Tarkista että kaikki välineet ovat kunnossa', 40, '2023-12-05', FALSE, FALSE),
(4, 6, 'Teknologiatarvikkeiden inventointi', 'Laske ja tarkista kaikki tarvikkeet', 60, '2023-12-10', TRUE, TRUE);

-- Insert example votes for two users
INSERT INTO votes (event_id, user_id, vote) VALUES
(1, 2, TRUE),
(1, 3, TRUE),
(1, 5, TRUE),
(1, 4, FALSE),
(3, 2, TRUE),
(3, 4, TRUE),
(4, 1, TRUE),
(4, 5, TRUE),
(5, 1, FALSE),
(5, 2, FALSE),
(5, 3, FALSE);

-- insert example confirmed scores
INSERT INTO confirmed_score_log (user_id, event_id, todo_id, score) VALUES
(1, null, 1, -50),
(2, null, 1, 50),
(6, null, 3, -30),
(1, null, 3, 30),
(4, null, 5, -60),
(6, null, 5, 60);