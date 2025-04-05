import sqlite3
import re
from rich.table import Table
from theme import console

DB_FILE = "commands.db"

def normalize_command(cmd):
    return cmd.strip().split()[0] if cmd.strip() else ""

def is_valid_command(cmd):
    base = normalize_command(cmd)
    return bool(re.match(r"^[\w./+!-]+$", base)) and base not in {"-", "..", ":", ":"}

def get_all_commands():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT command, count FROM commands ORDER BY command ASC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def display_table(data, title):
    table = Table(title=f"[header]{title}[/]", border_style="border")
    table.add_column("[header]Command", style="cell")
    table.add_column("[header]Count", style="cell", justify="right")
    for cmd, count in data:
        table.add_row(cmd, str(count))
    console.print(table)

def show_all_commands():
    commands = get_all_commands()
    if commands:
        summary = {}
        for cmd, count in commands:
            key = normalize_command(cmd)
            if is_valid_command(key):
                summary[key] = summary.get(key, 0) + count
        grouped = sorted(summary.items(), key=lambda x: x[0])
        display_table(grouped, "All Commands")
    else:
        console.print("[bold red]No commands found in the database.[/]")

def show_top_commands():
    try:
        console.print("\n[header]How many top commands do you want to see(defaule=10)?[/] [default: 10]")
        limit = int(input("> ") or 10)
    except ValueError:
        limit = 10

    commands = get_all_commands()
    if commands:
        summary = {}
        for cmd, count in commands:
            key = normalize_command(cmd)
            if is_valid_command(key):
                summary[key] = summary.get(key, 0) + count
        grouped = sorted(summary.items(), key=lambda x: x[1], reverse=True)[:limit]
        display_table(grouped, f"Top {limit} Commands")
    else:
        console.print("[bold red]No commands found in the database.[/]")

def main():
    while True:
        console.print("\n[bold underline]Command Stats Viewer[/]", style="header")
        console.print("[cell]1.[/] View Top Commands")
        console.print("[cell]2.[/] View All Commands")
        console.print("[cell]q.[/] Exit")

        choice = input("\n[>] ").strip()

        if choice == "1":
            show_top_commands()
        elif choice == "2":
            show_all_commands()
        elif choice == "q":
            console.print("[header]... Going back to main menu![/]")
            break
        else:
            console.print("[error]Invalid choice. Please try again.[/]")

if __name__ == "__main__":
    main()

