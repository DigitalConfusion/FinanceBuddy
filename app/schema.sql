DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS income;
DROP TABLE IF EXISTS expense;

CREATE TABLE user (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  total_balance FLOAT NOT NULL,
  total_income FLOAT NOT NULL,
  total_expense FLOAT NOT NULL,
  income_category TEXT NOT NULL,
  expense_category TEXT NOT NULL
);

CREATE TABLE income (
  expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  date INTEGER NOT NULL,
  amount FLOAT NOT NULL,
  category TEXT NOT NULL,
  description TEXT,
  FOREIGN KEY (user_id) REFERENCES user (user_id)
);

CREATE TABLE expense (
  expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  date INTEGER NOT NULL,
  amount FLOAT NOT NULL,
  category TEXT NOT NULL,
  description TEXT,
  FOREIGN KEY (user_id) REFERENCES user (user_id)
);
