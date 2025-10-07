#!/bin/bash

# Navigate to the script directory
cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Run with python3 (PyObjC handles the framework)
python3 nail_biting_detector.py
