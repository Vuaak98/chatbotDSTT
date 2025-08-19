#!/bin/bash

echo "==========================================="
echo "AI Math Chatbot - Repository Cleanup"
echo "==========================================="
echo

echo "Cleaning up Python cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
echo

echo "Cleaning up Python compiled files..."
find . -name "*.pyc" -delete 2>/dev/null
find . -name "*.pyo" -delete 2>/dev/null
echo

echo "Cleaning up database files..."
find . -name "*.db" -delete 2>/dev/null
find . -name "*.sqlite" -delete 2>/dev/null
find . -name "*.sqlite3" -delete 2>/dev/null
echo

echo "Cleaning up log files..."
find . -name "*.log" -delete 2>/dev/null
echo

echo "Cleaning up temporary files..."
find . -name "*.tmp" -delete 2>/dev/null
find . -name "*.temp" -delete 2>/dev/null
find . -name "*.bak" -delete 2>/dev/null
echo

echo "Cleaning up IDE files..."
rm -rf .vscode 2>/dev/null
rm -rf .idea 2>/dev/null
rm -rf .cursor 2>/dev/null
echo

echo "Repository cleanup completed!"
echo
echo "Next steps:"
echo "1. git add ."
echo "2. git commit -m \"feat: Complete AI Math Chatbot with RAG system\""
echo "3. git push origin main"
echo
