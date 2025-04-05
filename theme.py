from rich.console import Console
from rich.theme import Theme

# Gruvbox-inspired theme
gruvbox_theme = Theme({
    "header": "bold #fabd2f",    # yellow
    "border": "#928374",         # gray
    "cell": "#ebdbb2",           # light beige
    "error": "bold red"
})

console = Console(theme=gruvbox_theme)

