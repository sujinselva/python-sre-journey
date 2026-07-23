#!/bin/bash

if [ -z "$1" ]; then
    MSG="Update $(date '+%Y-%m-%d %H:%M:%S')"
else
    MSG="$1"
fi

git add .
git commit -m "$MSG"
git push origin main

echo ""
echo "✅ Push completed!"
