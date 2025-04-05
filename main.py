#!/usr/bin/env python3

import subprocess
import os
import sqlite3
from rich.panel import Panel
from rich.prompt import Prompt
from rich.layout import Layout
from theme import console

# Paths
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DB_FILE = os.path.join(BASE_DIR, "commands.db")
HISTORY_SCRIPT = os.path.join(BASE_DIR, "history.py")
VIEW_SCRIPT = os.path.join(BASE_DIR, "view_history.py")
CLEAR_DB_SCRIPT = os.path.join(BASE_DIR, "clear_db.py")

def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")

def database_exists():
    return os.path.exists(DB_FILE)

def get_command_stats():
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
        console.print(f"[error]Database error: {e}[/]")
        return (0, 0)

def show_initial_menu():
    menu_text = "[header bold]First Time Setup[/]\n\n"
    menu_text += "[header]1.[/] Import Shell History (initialize database)\n"
    menu_text += "[header]q.[/] Quit"
    return Panel(menu_text, title="[header]No Database Found[/]", border_style="border")

def show_full_menu():
    menu_text = "[header bold]Command Tracker Menu[/]\n\n"
    menu_text += "[header]1.[/] Update commands\n"
    menu_text += "[header]2.[/] View Commands\n"
    menu_text += "[header]3.[/] Clear Command History\n"
    menu_text += "[header]q.[/] Quit"
    return Panel(menu_text, title="[header]Main Menu[/]", border_style="border")

def show_stats_panel():
    if database_exists():
        total, unique = get_command_stats()
        content = f"[cell]Tracked Commands:[/] [header]{total}[/] total ([header]{unique}[/] unique)"
    else:
        content = "[error]⚠️  No database found. Please import history first."
    return Panel(content, title="[header]Stats[/]", border_style="border")

def first_time_menu():
    while True:
        clear_screen()
        layout = Layout()
        layout.split_column(
            Layout(show_stats_panel(), size=3),
            Layout(show_initial_menu(), size=8)
        )
        console.print(layout)

        choice = Prompt.ask("[prompt]Choose an option[/]", choices=["1", "q"], default="q")
        if choice == "1":
            subprocess.run(["python3", HISTORY_SCRIPT])
            input("\nPress Enter to continue...")
            break
        elif choice == "q":
            console.print("\n[header]Goodbye![/]")
            exit()

def main_menu():
    while True:
        clear_screen()
        layout = Layout()
        layout.split_column(
            Layout(show_stats_panel(), size=3),
            Layout(show_full_menu(), size=10)
        )
        console.print(layout)

        choice = Prompt.ask("[prompt]Choose an option[/]", choices=["1", "2", "3", "q"], default="q")

        if choice == "1":
            clear_choice = Prompt.ask("[prompt]Clear existing database before importing? (Not doing so will result in both old database and new entries getting appended)[/]", choices=["y", "n"], default="y")
            if clear_choice == "y":
                subprocess.run(["python3", CLEAR_DB_SCRIPT])
            subprocess.run(["python3", HISTORY_SCRIPT])
            input("\nPress Enter to return to menu...")

        elif choice == "2":
            subprocess.run(["python3", VIEW_SCRIPT])
            input("\nPress Enter to return to menu...")

        elif choice == "3":
            confirm = Prompt.ask("[prompt]Delete all command history?[/]", choices=["y", "n"], default="n")
            if confirm == "y":
                subprocess.run(["python3", CLEAR_DB_SCRIPT])
                console.print("[header]✅ Database cleared successfully.[/]")
            else:
                console.print("[cell]Cancelled.[/]")
            input("\nPress Enter to return to menu...")

        elif choice == "q":
            console.print("\n[header]Goodbye![/]")
            break

if __name__ == "__main__":
    if not database_exists():
        first_time_menu()
    main_menu()

