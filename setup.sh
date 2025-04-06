#!/bin/bash

set -e

echo "🔧 Setting up Command Tracker (Arch Linux friendly)..."

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "❌ Python3 is not installed."
    exit 1
fi

# Create virtual environment
echo "🐍 Creating virtual environment..."
python3 -m venv .venv

# Activate it and install dependencies
echo "📦 Installing Python dependencies inside virtual environment..."
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create symlink for 'showcmm'
echo "🔗 Adding 'showcmm' command..."
chmod +x main.py
sudo ln -sf "$(pwd)/main.py" /usr/local/bin/showcmm

# Install man page
MAN_PAGE="showcmm.1"
MAN_DIR="/usr/local/share/man/man1"

if [[ -f "$MAN_PAGE" ]]; then
    echo "📘 Installing man page..."
    sudo mkdir -p "$MAN_DIR"
    sudo cp "$MAN_PAGE" "$MAN_DIR/"
    sudo gzip -f "$MAN_DIR/$MAN_PAGE"
    echo "✅ Man page installed."
else
    echo "⚠️  No man page found. Skipping."
fi

echo "✅ Setup complete!"
echo "👉 Run the app using: showcmm"
echo "👉 If you want to use the virtual environment manually, run: source .venv/bin/activate"

