CREATE DATABASE logs_db;
CREATE DATABASE users_db;

\connect users_db

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL
);

\connect logs_db

CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    action VARCHAR(50) NOT NULL,
    username VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
