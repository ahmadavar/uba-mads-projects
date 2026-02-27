#!/bin/bash

# Simple script to launch the Jupyter Notebook

echo "=========================================="
echo "  Statistical Regression Analysis"
echo "=========================================="
echo ""
echo "Starting Jupyter Notebook..."
echo ""

cd ~/stats_regression_project
source venv/bin/activate

# Check if running in a display environment
if [ -z "$DISPLAY" ]; then
    echo "No display detected - launching without browser"
    echo "Copy the URL shown below and paste in your browser"
    echo ""
    jupyter notebook --no-browser --port=8888
else
    echo "Launching Jupyter in your browser..."
    jupyter notebook
fi
