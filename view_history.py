import sqlite3
import re
import os
import sys
from rich.table import Table
from rich.console import Group
from rich.panel import Panel
from rich.progress import BarColumn, Progress
from rich.text import Text
from theme import console

# Get absolute path to database file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "commands.db")

def normalize_command(cmd):
    return cmd.strip().split()[0] if cmd.strip() else ""

def is_valid_command(cmd):
    base = normalize_command(cmd)
    return bool(re.match(r"^[a-zA-Z0-9._/+!-]+$", base)) and base not in {"-", "..", ":", ":"}

def get_all_commands():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT command, count FROM commands ORDER BY command ASC")
        rows = cursor.fetchall()
        conn.close()
        return rows
    except sqlite3.OperationalError as e:
        console.print(f"[bold red]Database error:[/] {e}")
        return []

def display_table(data, title):
    table = Table(title=f"[header]{title}[/]", border_style="border")
    table.add_column("[header]Command", style="cell")
    table.add_column("[header]Count", style="cell", justify="right")
    for cmd, count in data:
        table.add_row(cmd, str(count))
    console.print(table)

def display_bar_graph(data, title):
    if not data:
        console.print("[bold red]No data to display.[/]")
        return

    max_count = max(count for _, count in data)
    bars = [
        f"[cell]{cmd:<15}[/] [header]{'█' * int((count / max_count) * 30)}[/] [cell]{count}[/]"
        for cmd, count in data
    ]
    console.print(Panel("\n".join(bars), title=f"[header]{title}[/]", border_style="border"))

def filter_commands(commands, query):
    query = query.strip().lower()
    return [(cmd, count) for cmd, count in commands if query in normalize_command(cmd).lower()]

def show_all_commands():
    commands = get_all_commands()
    if not commands:
        console.print("[bold red]No commands found in the database.[/]")
        return

    summary = {}
    for cmd, count in commands:
        key = normalize_command(cmd)
        if is_valid_command(key):
            summary[key] = summary.get(key, 0) + count
    grouped = sorted(summary.items(), key=lambda x: x[0])

    display_table(grouped, "\n All Commands")

    show_graph = input("Show graph? [y/N]: ").strip().lower()
    if show_graph == "y":
        display_bar_graph(grouped[:20], "Command Usage")

def show_top_commands():
    try:
        limit = int(input("How many top commands do you want to see? [Default: 10]: ") or 10)
    except ValueError:
        limit = 10

    commands = get_all_commands()
    if not commands:
        console.print("[bold red]No commands found in the database.[/]")
        return

    summary = {}
    for cmd, count in commands:
        key = normalize_command(cmd)
        if is_valid_command(key):
            summary[key] = summary.get(key, 0) + count

    grouped = sorted(summary.items(), key=lambda x: x[1], reverse=True)[:limit]
    display_table(grouped, f"\n Top {limit} Commands")

    show_graph = input("Show graph? [y/N]: ").strip().lower()
    if show_graph == "y":
        display_bar_graph(grouped, f"Top {limit} Commands Usage")


def show_filtered_commands(query=None):
    if query is None:
        query = input("Enter part of the command to filter by: ").strip().lower()
    if not query:
        console.print("[bold red]No filter provided.[/]")
        return

    commands = get_all_commands()
    summary = {}
    for cmd, count in commands:
        if query in cmd.lower():
            key = normalize_command(cmd)
            if is_valid_command(key):
                summary[cmd] = summary.get(cmd, 0) + count

    if not summary:
        console.print(f"[bold red]No matching commands found for '{query}'.[/]")
        return

    grouped = sorted(summary.items(), key=lambda x: x[1], reverse=True)
    display_table(grouped, f"Filtered by '{query}'")

    show_graph = input("Show graph? [y/N]: ").strip().lower()
    if show_graph == "y":
        display_bar_graph(grouped[:20], f"Command Usage (Filtered: {query})")

def main():
    while True:
        console.print("\n[bold underline]Command Stats Viewer[/]", style="header")
        print("1. View Top Commands")
        print("2. View All Commands")
        print("3. Filter Commands")
        print("q. Exit")

        choice = input("\nChoose an option [Default: q]: ").strip().lower() or "q"

        if choice == "1":
            show_top_commands()
        elif choice == "2":
            show_all_commands()
        elif choice == "3":
            show_filtered_commands()
        elif choice == "q":
            print("Going back to main menu!")
            break
        else:
            print("Invalid choice. Please try again.")

def cli_entry():
    args = sys.argv[1:]

    if "--top" in args:
        show_top_commands()
    elif "--all" in args:
        show_all_commands()
    elif "--filter" in args:
        try:
            idx = args.index("--filter")
            query = args[idx + 1]
            show_filtered_commands(query)
        except (IndexError, ValueError):
            console.print("[bold red]Please provide a command to filter after '--filter'[/]")
    else:
        main()

if __name__ == "__main__":
    cli_entry()

