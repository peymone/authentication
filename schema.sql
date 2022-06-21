CREATE TABLE IF NOT EXISTS users (
    email TEXT UNIQUE NOT NULL,
    confirmed_email TEXT NOT NULL,
    login TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL 
);