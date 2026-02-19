#!/bin/bash

# AdorLipi Installation Script

echo "Checking for Python 3..."
if ! command -v python3 &> /dev/null
then
    echo "Python 3 could not be found. Please install python3."
    exit 1
fi

echo "Installing AdorLipi..."

# Check if pip is available
if ! command -v pip3 &> /dev/null
then
    echo "pip3 not found. Installing pip..."
    if [ -f /etc/debian_version ]; then
        sudo apt update && sudo apt install -y python3-pip
    elif [ -f /etc/redhat-release ]; then
        sudo dnf install -y python3-pip
    else
        echo "Please install python3-pip manually."
        exit 1
    fi
fi

# Install the package
pip3 install .

if [ $? -eq 0 ]; then
    echo "-----------------------------------"
    echo "AdorLipi installed successfully!"
    echo "Run 'adorlipi' to start the engine."
    echo "-----------------------------------"
else
    echo "Installation failed."
fi
