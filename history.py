import os
import re
import subprocess
from cmd_database import insert_commands_bulk

def list_available_shells():
    shells = {
        "bash": os.path.expanduser("~/.bash_history"),
        "zsh": os.path.expanduser("~/.zsh_history"),
        "fish": os.path.expanduser("~/.local/share/fish/fish_history")
    }
    return {shell: path for shell, path in shells.items() if os.path.exists(path)}

def run_shell_command(command):
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"Error executing command: {e}")
        return None

def choose_shells():
    available_shells = list_available_shells()
    if not available_shells:
        print("No history files found.")
        return []

    print("Available shell histories:")
    for i, shell in enumerate(available_shells, 1):
        print(f"{i}. {shell} ({available_shells[shell]})")
    print("0. All shells")

    choice = input("Choose a shell (number or multiple numbers separated by space): ").strip()
    if choice == "0":
        return list(available_shells.values())

    try:
        choices = [int(c) - 1 for c in choice.split()]
        paths = list(available_shells.values())
        return [paths[c] for c in choices if 0 <= c < len(paths)]
    except (ValueError, IndexError):
        print("Invalid choice.")
        return []


def is_valid_command(command):
    # Ignore empty lines, dashes, or words like 'and:' that are clearly not commands
    if not command or command.strip() == "-" or command.strip().lower() in {"and:", "or:", "then:", "fi", "do", "done"}:
        return False
    # Filter out anything that doesn’t start with a command-like character
    return re.match(r'^[a-zA-Z0-9./]', command) is not None


def read_history():
    history_files = choose_shells()
    if not history_files:
        return []

    commands = []
    batch = []
    batch_size = 100

    for file_path in history_files:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            for line in file:
                command = re.sub(r'^: \d+:\d+;', '', line.strip())
                if is_valid_command(command):
                    batch.append(command)

                if len(batch) >= batch_size:
                    insert_commands_bulk(batch)
                    commands.extend(batch)
                    batch = []

    if batch:
        insert_commands_bulk(batch)
        commands.extend(batch)

    return commands

if __name__ == "__main__":
    shell_type = run_shell_command("echo $SHELL")
    print(f"Detected Shell: {shell_type}")
    commands = read_history()
    if commands:
        print("\nLast 10 commands from selected shell(s):")
        print("\n".join(commands[:10]))
    else:
        print("No history found.")
