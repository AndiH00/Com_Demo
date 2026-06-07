#!/bin/bash

set -e

VENV_DIR=".venv"
SCRIPTS_DIR="scripts"
REQUIREMENTS_FILE="requirements.txt"

echo "=== Python Virtual Environment Setup ==="

# Clean flag check
if [ "$1" = "clean" ]; then
    echo "Removing existing virtual environment..."
    if [ -d "$VENV_DIR" ]; then
        rm -rf "$VENV_DIR"
        echo "✓ Virtual environment removed."
    else
        echo "ℹ No virtual environment found to clean."
    fi
fi

# Create venv if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    echo "✓ Virtual environment created."
else
    echo "ℹ Virtual environment already exists."
fi

# Activate venv
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"
echo "✓ Virtual environment activated."

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements if file exists
if [ -f "$SCRIPTS_DIR/$REQUIREMENTS_FILE" ]; then
    echo "Installing requirements from $SCRIPTS_DIR/$REQUIREMENTS_FILE..."
    pip install -r "$SCRIPTS_DIR"/"$REQUIREMENTS_FILE"
    echo "✓ Requirements installed."
else
    echo "⚠ No $REQUIREMENTS_FILE found."
fi

# Check Python scripts in scripts directory
if [ -d "$SCRIPTS_DIR" ]; then
    echo "Scanning Python scripts in $SCRIPTS_DIR..."
    for script in "$SCRIPTS_DIR"/*.py; do
        if [ -f "$script" ]; then
            echo "  • Found: $(basename "$script")"
        fi
    done
fi

echo ""
echo "=== Setup Complete ==="
echo "Virtual environment is now active!"
echo "To deactivate later, run: deactivate"
echo ""