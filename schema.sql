-- ─────────────────────────────────────────────────────────
-- Farmer Market Price Information System — schema.sql
-- Run this to manually set up the SQLite database:
--   sqlite3 database.db < schema.sql
-- ─────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS crop_prices (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    crop_name       TEXT    NOT NULL,
    price_per_kg    REAL    NOT NULL,
    market_location TEXT    NOT NULL,
    date            TEXT    NOT NULL
);

INSERT INTO crop_prices (crop_name, price_per_kg, market_location, date) VALUES
    ('Rice',      28.50, 'Chennai Market',    date('now')),
    ('Wheat',     22.00, 'Salem APMC',        date('now')),
    ('Tomato',    18.75, 'Coimbatore Mandi',  date('now')),
    ('Potato',    15.00, 'Bangalore Market',  date('now')),
    ('Onion',     20.30, 'Nasik Wholesale',   date('now')),
    ('Maize',     14.50, 'Trichy Mandi',      date('now')),
    ('Soybean',   45.00, 'Indore APMC',       date('now')),
    ('Sugarcane',  3.80, 'Erode Market',      date('now'));
