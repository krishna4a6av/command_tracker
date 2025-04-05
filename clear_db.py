import os

DB_FILE = "commands.db"

def clear_database_file():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print("Database file removed successfully.")
    else:
        print("No database file found to remove.")

if __name__ == "__main__":
    clear_database_file()

