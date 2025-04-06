# 🛠 Setup

Clone the repo and run the setup script:

```bash
git clone https://github.com/krishna4a6av/command_tracker.git
cd command_tracker
chmod +x setup.sh
./setup.sh
```

If pip fails to  install tabulate or any other dependency on your os you can install them through your package manager.


To remove:
```bash
cd command_tracker
chmod +x uninstall.sh
./uninstall.sh
```

I made this as a project for fun, simply to be able to see most used commands and other command line stats. This project is entirely made in python, hence easy to modify depending on anyones preferences.

Main feature include:
 - Allowing to see command history in tabular form from all shells(bash/zsh/fish)
 - extensive elaboration on commandline habbits 
 - Allowing one to track most used commands with style (Gruvbox theme)


Dependencies you might need (Not needed to be added manually, setup.sh will take care of them)
  - python, pip, tabulate (pip install tabulate, python-tabulate on aur)


Future plan
  - Adding graphs
  - More themes maybe
  - Gui? maybe


Plase feel free to clone/fork this simple proj and adding your twists :)
