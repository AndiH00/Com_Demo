#!/bin/bash

set -e

VENV_PYTHON=".venv/bin/python"
SCRIPT_PATH="scripts/commander_gui.py"
VENV_DIR=".venv"

echo "=== Commander GUI Launcher ==="

# Check if venv exists
if [ ! -d "$VENV_DIR" ]; then
    echo "✗ Error: Virtual environment not found at $VENV_DIR"
    echo "Please run ./setup_venv.sh first"
    exit 1
fi

# Check if venv python exists
if [ ! -f "$VENV_PYTHON" ]; then
    echo "✗ Error: Python executable not found at $VENV_PYTHON"
    echo "Virtual environment may be corrupted. Run './setup_venv.sh clean' to reinstall"
    exit 1
fi

# Check if script exists
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "✗ Error: Script not found at $SCRIPT_PATH"
    exit 1
fi

# Verify python interpreter works
if ! "$VENV_PYTHON" --version > /dev/null 2>&1; then
    echo "✗ Error: Python interpreter not working"
    exit 1
fi

echo "✓ Virtual environment found"
echo "✓ Python executable verified"
echo "✓ Script found at $SCRIPT_PATH"
echo ""
echo "Starting Commander GUI..."
echo ""

# Run the script
"$VENV_PYTHON" "$SCRIPT_PATH" &