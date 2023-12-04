#!/bin/bash
# Check if requirements.txt file exists
if [ -f "requirements.txt" ]; then
    # Install Python dependencies
    pip install -r requirements.txt
else
    echo "requirements.txt file not found."
fi