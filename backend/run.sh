#!/bin/bash

# Simple script to run the backend server

echo "Starting Hackathon Presentation Generator Backend..."
echo "Make sure you have set ANTHROPIC_API_KEY in your .env file"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Please create a .env file with your ANTHROPIC_API_KEY"
    echo ""
    echo "Example:"
    echo "ANTHROPIC_API_KEY=sk-ant-api03-xxxxx"
    echo "GITHUB_TOKEN=ghp_xxxxx  # Optional"
    echo ""
    exit 1
fi

# Run with Python directly (no venv needed if packages are installed globally)
python3 main.py

