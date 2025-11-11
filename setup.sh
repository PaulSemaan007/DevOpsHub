#!/bin/bash

echo "========================================"
echo "DevOpsHub Setup (Mac/Linux)"
echo "========================================"
echo ""

echo "[1/4] Creating virtual environment..."
python3 -m venv .venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    echo "Please ensure Python 3.8+ is installed"
    exit 1
fi

echo "[2/4] Activating virtual environment..."
source .venv/bin/activate

echo "[3/4] Upgrading pip..."
python -m pip install --upgrade pip

echo "[4/4] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To run DevOpsHub:"
echo "  1. Activate virtual environment: source .venv/bin/activate"
echo "  2. Run the app: streamlit run app.py"
echo ""
