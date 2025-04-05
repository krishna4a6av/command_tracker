import subprocess
import os
import sqlite3

# Get absolute path to the project directory (where main.py is located)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "commands.db")
HISTORY_SCRIPT = os.path.join(BASE_DIR, "history.py")
VIEW_SCRIPT = os.path.join(BASE_DIR, "view_history.py")
CLEAR_DB_SCRIPT = os.path.join(BASE_DIR, "clear_db.py")

def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")

def database_exists():
    return os.path.exists(DB_FILE)

def get_command_stats():
    if not database_exists():
        return (0, 0)
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM commands")
        total_unique = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(count) FROM commands")
        total = cursor.fetchone()[0] or 0

        conn.close()
        return total, total_unique
    except sqlite3.Error as e:
        print(f"Error reading from database: {e}")
        return (0, 0)

def main_menu():
    while True:
        clear_screen()
        print("=== Command Tracker ===")

        if database_exists():
            total, unique = get_command_stats()
            print(f"Tracked Commands: {total} total ({unique} unique)\n")
        else:
            print("⚠️  No command history found. Please import shell history.\n")

        print("1. Import Shell History")
        print("2. View Commands")
        print("3. Clear Command history")
        print("e. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            if database_exists():
                clear_choice = input("Do you want to clear the existing database before importing? (not doing so will end up in old history and newly imported history getting appended) [y/N]: ").strip().lower()
                if clear_choice == "y":
                    subprocess.run(["python3", CLEAR_DB_SCRIPT])
            subprocess.run(["python3", HISTORY_SCRIPT])
            input("\nPress Enter to return to menu...")

        elif choice == "2":
            if not database_exists():
                print("⚠️  You need to import shell history first.")
            else:
                subprocess.run(["python3", VIEW_SCRIPT])
            input("\nPress Enter to return to menu...")

        elif choice == "3":
            if not database_exists():
                print("⚠️  Database does not exist.")
            else:
                confirm = input("Are you sure you want to delete all command history from the database? [y/N]: ").strip().lower()
                if confirm == "y":
                    subprocess.run(["python3", CLEAR_DB_SCRIPT])
                    print("✅ Database cleared successfully.")
                else:
                    print("Cancelled.")
            input("\nPress Enter to return to menu...")

        elif choice == "e":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")
            input("Press Enter to try again...")


if __name__ == "__main__":
    main_menu()
