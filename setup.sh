#!/bin/bash

echo "🔧 Setting up Command Tracker..."

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "❌ Python3 is not installed. Please install it and re-run this script."
    exit 1
fi

# Check pip
if ! command -v pip3 &>/dev/null; then
    echo "❌ pip3 is not installed. Please install it and re-run this script."
    exit 1
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Create symlink for 'showcmm'
echo "🔗 Adding 'showcmm' command..."
chmod +x main.py
sudo ln -sf "$(pwd)/main.py" /usr/local/bin/showcmm

echo "✅ Setup complete. You can now run 'showcmm' from anywhere!"

