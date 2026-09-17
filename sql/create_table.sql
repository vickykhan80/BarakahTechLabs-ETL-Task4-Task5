CREATE TABLE IF NOT EXISTS api_posts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    title TEXT,
    body TEXT,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
