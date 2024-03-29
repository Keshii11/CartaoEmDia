CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    invoice_day INTEGER NOT NULL DEFAULT -1
);

CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    date DATE NOT NULL,
    name TEXT NOT NULL,
    installments INTEGER NOT NULL,
    total REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
