import sqlite3

def init_db():
    conn = sqlite3.connect("database/game.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS game_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_move TEXT,
        computer_move TEXT,
        winner TEXT
    )
    """)

    conn.commit()
    conn.close()

def insert_game(player, computer, winner):
    conn = sqlite3.connect("database/game.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO game_history (player_move, computer_move, winner)
    VALUES (?, ?, ?)
    """, (player, computer, winner))

    conn.commit()
    conn.close()