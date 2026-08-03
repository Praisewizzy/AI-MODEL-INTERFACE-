#!/bin/bash

echo "Repairing Termux package directory structure..."
# Re-create missing apt archive cache folders if Android cleared them
mkdir -p /data/data/com.termux/cache/apt/archives/partial

echo "Updating Termux repositories and installing Python..."
# Fix broken or missing packages gracefully
pkg update -y --fix-missing || apt-get update --fix-missing
pkg install python -y || apt-get install python -y

echo "Installing OpenAI python package..."
pip install openai

# Setup shortcut alias 'ai'
echo "alias ai='python ~/AI-MODEL-INTERFACE-/app.py'" >> ~/.bashrc

echo ""
echo "Setup complete!"
echo "Run: source ~/.bashrc"
echo "Then type 'ai' to launch."
