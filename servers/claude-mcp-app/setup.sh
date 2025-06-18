#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Setting up Claude MCP Data Analysis Tool"
echo "========================================"

# Create a virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install Python dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Verify installation
echo "Verifying installation..."
python -c "import mcp; print(f'MCP version: {mcp.__version__}')"
python -c "import pandas; print(f'Pandas version: {pandas.__version__}')"
python -c "import numpy; print(f'NumPy version: {numpy.__version__}')"
python -c "import httpx; print(f'HTTPX version: {httpx.__version__}')"

# Make the run script executable
chmod +x run_server.sh
chmod +x test_suite.py

echo ""
echo "Setup complete! You can now run the MCP server with:"
echo "./run_server.sh"
echo ""
echo "To test the server, run:"
echo "./test_suite.py --start-server"
echo ""
