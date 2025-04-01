import os
import re
import subprocess


def list_available_shells():
    """Lists available shell history files, including Bash, Zsh, and Fish."""
    shells = {

            #add any other shell or different path (if you have) to shell history below

        "bash": os.path.expanduser("~/.bash_history"),
        "zsh": os.path.expanduser("~/.zsh_history"),
        "fish": os.path.expanduser("~/.local/share/fish/fish_history")
    }
    available = {shell: path for shell, path in shells.items() if os.path.exists(path)}
    return available



def run_shell_command(command):
    """Executes a shell command and returns the output."""
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"Error executing command: {e}")
        return None



def choose_shell():
    """Allows the user to choose which shell history to read from."""
    available_shells = list_available_shells()
    if not available_shells:
        print("No history files found for supported shells.")
        return None
    
    print("Available shell histories:")
    for i, shell in enumerate(available_shells, 1):
        print(f"{i}. {shell} ({available_shells[shell]})")
    print("0. All shells")
    
    choice = input("\n Choose a shell (number or multiple numbers separated by space): ").strip()
    
    if choice == "0":
        return list(available_shells.values())
    
    try:
        choices = [int(c) - 1 for c in choice.split()]

        shell_paths = list(available_shells.values())  # Get shell history paths
        selected_shells = []  # List to store selected paths

        for c in choices:
            if c in range(len(shell_paths)):  # Ensure valid index
                selected_shells.append(shell_paths[c])  # Append valid selection


        #alternatively to above code block selected_shells = [list(available_shells.values())[c] for c in choices if c in range(len(available_shells))]
        return selected_shells
    except (ValueError, IndexError):
        print("Invalid choice.")
        return []


def read_history():
    """Reads command history from user-selected shell history files."""
    history_files = choose_shell()
    if not history_files:
        return []
    
    commands = []
    for history_file in history_files:
        with open(history_file, "r", encoding="utf-8", errors="ignore") as file:
            lines = file.readlines()
        
        # Clean Zsh history (remove timestamps)
        cleaned_history = [re.sub(r'^: \d+:\d+;', '', line.strip()) for line in lines]
        commands.extend(cleaned_history)
    
    return commands


if __name__ == "__main__":
    shell_type = run_shell_command("echo $SHELL")
    print(f"shell being used : {shell_type}\n")
    
    commands = read_history()
    if commands != []:
        print("\n last 10 commands in chosen shell: \n")
        print("\n".join(commands[:10]))  # Print first 10 commands for preview
    else:
        print("No history avilable")

