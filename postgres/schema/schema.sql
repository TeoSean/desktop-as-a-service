CREATE TABLE users (
    id TEXT UNIQUE NOT NULL,
    username TEXT UNIQUE NOT NULL,
    hash TEXT NOT NULL,
    token TEXT NOT NULL
);

CREATE TABLE sessions (
    id TEXT UNIQUE NOT NULL,
    token TEXT UNIQUE NOT NULL,
    expiration INT NOT NULL,
);

CREATE TABLE instances (
    id TEXT UNIQUE NOT NULL,
    userid TEXT UNIQUE NOT NULL,
    paused BOOLEAN NOT NULL,
    created_at INT NOT NULL,
);

CREATE TABLE images (
    id TEXT UNIQUE NOT NULL,
    lesson_id UNIQUE NOT NULL,
    created_at INT NOT NULL
)
