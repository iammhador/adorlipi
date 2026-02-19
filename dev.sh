#!/bin/bash

# Development Run Script
# Syncs changes from banglish_mvp if it exists (legacy support)
if [ -d "banglish_mvp" ]; then
    echo "Syncing changes from banglish_mvp to adorlipi..."
    cp -u banglish_mvp/data/*.json adorlipi/data/ 2>/dev/null
fi

# Set PYTHONPATH to current directory so we can import 'adorlipi' package
export PYTHONPATH=$PYTHONPATH:$(pwd)

echo "Starting AdorLipi (Dev Mode)..."
python3 adorlipi/main.py
