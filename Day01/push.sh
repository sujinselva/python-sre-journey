#!/bin/bash

echo "========================================"
echo "Git Push Helper"
echo "========================================"

cd ~/Projects/python-sre-journey || exit

echo
echo "Git Status:"
git status

echo
read -p "Enter commit message: " MESSAGE

if [ -z "$MESSAGE" ]; then
    echo "Commit message cannot be empty."
    exit 1
fi

echo
git add .

git commit -m "$MESSAGE"

if [ $? -ne 0 ]; then
    echo
    echo "Nothing to commit."
    exit 0
fi

echo
git push

echo
echo "Checking GitHub Actions..."
sleep 3

gh run list --limit 1

echo
echo "Done! 🚀"
