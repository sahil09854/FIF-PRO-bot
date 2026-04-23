import sqlite3
import os

DB_PATH = "football.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        coins INTEGER DEFAULT 500,
        wins INTEGER DEFAULT 0,
        losses INTEGER DEFAULT 0,
        draws INTEGER DEFAULT 0
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS user_players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        player_name TEXT,
        position TEXT,
        rating INTEGER,
        pace INTEGER,
        shooting INTEGER,
        passing INTEGER,
        dribbling INTEGER,
        defending INTEGER,
        physical INTEGER,
        rarity TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS dream_team (
        user_id INTEGER PRIMARY KEY,
        gk INTEGER,
        def1 INTEGER,
        def2 INTEGER,
        def3 INTEGER,
        def4 INTEGER,
        mid1 INTEGER,
        mid2 INTEGER,
        mid3 INTEGER,
        fwd1 INTEGER,
        fwd2 INTEGER,
        fwd3 INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS battles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        challenger_id INTEGER,
        opponent_id INTEGER,
        status TEXT DEFAULT 'pending',
        winner_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS drafts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        challenger_id INTEGER,
        opponent_id INTEGER,
        challenger_picks TEXT,
        opponent_picks TEXT,
        status TEXT DEFAULT 'pending',
        winner_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    conn.commit()
    conn.close()
    print("✅ Database initialized!")

def ensure_user(user_id, username):
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def update_coins(user_id, amount):
    conn = get_conn()
    c = conn.cursor()
    c.execute("UPDATE users SET coins = coins + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()
    conn.close()

def add_player_to_user(user_id, player):
    conn = get_conn()
    c = conn.cursor()
    c.execute('''INSERT INTO user_players 
        (user_id, player_name, position, rating, pace, shooting, passing, dribbling, defending, physical, rarity)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (user_id, player['name'], player['position'], player['rating'],
         player['pace'], player['shooting'], player['passing'],
         player['dribbling'], player['defending'], player['physical'], player['rarity']))
    conn.commit()
    conn.close()

def get_user_players(user_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM user_players WHERE user_id = ?", (user_id,))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_match_result(winner_id, loser_id, is_draw=False):
    conn = get_conn()
    c = conn.cursor()
    if is_draw:
        c.execute("UPDATE users SET draws = draws + 1 WHERE user_id = ?", (winner_id,))
        c.execute("UPDATE users SET draws = draws + 1 WHERE user_id = ?", (loser_id,))
    else:
        c.execute("UPDATE users SET wins = wins + 1 WHERE user_id = ?", (winner_id,))
        c.execute("UPDATE users SET losses = losses + 1 WHERE user_id = ?", (loser_id,))
    conn.commit()
    conn.close()
