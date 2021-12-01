-- SQLite

CREATE TABLE users (id INTEGER PRIMARY KEY, email text NOT NULL UNIQUE, password_hash text NOT NULL);

DELETE FROM payments WHERE id = 3;

CREATE TABLE payments(id INTEGER PRIMARY KEY, card TEXT, day INTEGER, month INTEGER, year INTEGER, type TEXT, amount REAL, user_id INTEGER, FOREIGN KEY(user_id) REFERENCES users(id));

CREATE TABLE planning (id INTEGER PRIMARY KEY, month TEXT, year TEXT, monthly_salary REAL, monthly_saving REAL, user_id INTEGER, FOREIGN KEY(user_id) REFERENCES users(ID));

DROP TABLE payments;

SELECT email FROM users WHERE email = ?


                <th>{{ all_queries_plan[x][4] - payments[x][0] - all_queries_plan[x][5] }}</th>
                <th>{{ all_queries_plan[x][4] - payments[x][0] }}</th>