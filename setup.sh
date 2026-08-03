#!/bin/bash

echo "Installing required packages in Termux..."
pkg update && pkg install python git -y
pip install openai

# Create shortcut alias 'ai' to run the python app
echo "alias ai='python ~/app.py'" >> ~/.bashrc

echo ""
echo "Setup complete!"
echo "Run 'source ~/.bashrc' or restart Termux."
echo "Then type 'ai' to start — it will prompt you for your own API key on the first run."
