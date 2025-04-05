import sqlite3
from tabulate import tabulate

DB_FILE = "commands.db"

# Normalize commands by extracting the base command (e.g., 'cd' from 'cd Documents')
def normalize_command(cmd):
    return cmd.strip().split()[0] if cmd.strip() else ""

def get_all_commands():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT command, count FROM commands ORDER BY command ASC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_top_commands(limit=10):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT command, count FROM commands ORDER BY count DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def show_all_commands():
    print("\nAll Commands:\n")
    commands = get_all_commands()
    if commands:
        # Group by normalized command
        summary = {}
        for cmd, count in commands:
            key = normalize_command(cmd)
            if key:
                summary[key] = summary.get(key, 0) + count
        grouped = sorted(summary.items(), key=lambda x: x[0])
        print(tabulate(grouped, headers=["Command", "Count"], tablefmt="fancy_grid"))
    else:
        print("No commands found in the database.")

def show_top_commands():
    try:
        limit = int(input("How many top commands do you want to see? [Default: 10]: ") or 10)
    except ValueError:
        limit = 10

    print(f"\nTop {limit} Commands:\n")
    commands = get_all_commands()
    if commands:
        # Group by normalized command and get top N
        summary = {}
        for cmd, count in commands:
            key = normalize_command(cmd)
            if key:
                summary[key] = summary.get(key, 0) + count
        grouped = sorted(summary.items(), key=lambda x: x[1], reverse=True)[:limit]
        print(tabulate(grouped, headers=["Command", "Count"], tablefmt="fancy_grid"))
    else:
        print("No commands found in the database.")

def main():
    while True:
        print("\nCommand Stats Viewer")
        print("====================")
        print("1. View Top Commands")
        print("2. View All Commands")
        print("e. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            show_top_commands()
        elif choice == "2":
            show_all_commands()
        elif choice == "e":
            print("Going back to main menu!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
