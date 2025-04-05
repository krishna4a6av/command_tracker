import sqlite3

DB_FILE = "commands.db"

def get_db_connection():
    """Creates and returns a database connection."""
    return sqlite3.connect(DB_FILE)

def initialize_database():
    """Creates the commands table if it doesn't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS commands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            command TEXT UNIQUE,
            count INTEGER DEFAULT 1
        )
    """)
    conn.commit()
    conn.close()

def insert_commands_bulk(commands):
    """Inserts multiple commands into the database at once for efficiency."""
    conn = get_db_connection()
    cursor = conn.cursor()

    for command in commands:
        cursor.execute("""
            INSERT INTO commands (command, count)
            VALUES (?, 1)
            ON CONFLICT(command) DO UPDATE SET count = count + 1
        """, (command,))

    conn.commit()
    conn.close()

# Ensure table exists when module is imported
initialize_database()
