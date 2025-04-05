#!/bin/bash

# Uninstall script for command_tracker

echo "🔧 Uninstalling Command Tracker..."

# Remove symbolic link
if [ -L /usr/local/bin/showcmm ]; then
    sudo rm /usr/local/bin/showcmm
    echo "✅ Removed 'showcmm' command from /usr/local/bin"
else
    echo "⚠️ 'showcmm' symlink not found in /usr/local/bin"
fi

# Optionally, ask to remove the cloned project directory
read -p "Do you want to remove the command_tracker project folder? (y/N): " del_proj
if [[ "$del_proj" == "y" || "$del_proj" == "Y" ]]; then
    proj_dir=$(dirname "$(realpath "$0")")
    echo "Deleting $proj_dir..."
    rm -rf "$proj_dir"
    echo "✅ Project folder removed."
else
    echo "Skipping project folder removal."
fi

echo "🎉 Uninstallation complete."

