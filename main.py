import subprocess
import os
import sqlite3
from theme import console

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
        console.print(f"[error]Error reading from database: {e}[/]")
        return (0, 0)

def main_menu():
    while True:
        clear_screen()
        console.print("=== [header]Command Tracker[/] ===\n")

        if database_exists():
            total, unique = get_command_stats()
            console.print(f"[cell]Tracked Commands:[/] [header]{total}[/] total ([header]{unique}[/] unique)\n")
        else:
            console.print("[error]⚠️  No command history found. Please import shell history.[/]\n")

        console.print("[header]1.[/] Import Shell History")
        console.print("[header]2.[/] View Commands")
        console.print("[header]3.[/] Clear Command History")
        console.print("[header]q.[/] Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            if database_exists():
                clear_choice = input("Clear existing database before importing? (importing new history files without clearing old will end up in both getting appended) [y/N]: ").strip().lower()
                if clear_choice == "y":
                    subprocess.run(["python3", CLEAR_DB_SCRIPT])
            subprocess.run(["python3", HISTORY_SCRIPT])
            input("\nPress Enter to return to menu...")

        elif choice == "2":
            if not database_exists():
                console.print("[error]⚠️  You need to import shell history first.[/]")
            else:
                subprocess.run(["python3", VIEW_SCRIPT])
            input("\nPress Enter to return to menu...")

        elif choice == "3":
            if not database_exists():
                console.print("[error]⚠️  Database does not exist.[/]")
            else:
                confirm = input("Are you sure you want to delete all command history from the database? [y/N]: ").strip().lower()
                if confirm == "y":
                    subprocess.run(["python3", CLEAR_DB_SCRIPT])
                    console.print("[header]✅ Database cleared successfully.[/]")
                else:
                    console.print("[cell]Cancelled.[/]")
            input("\nPress Enter to return to menu...")

        elif choice == "q":
            console.print("[header]Goodbye![/]")
            break
        else:
            console.print("[error]Invalid option.[/]")
            input("Press Enter to try again...")

if __name__ == "__main__":
    main_menu()

