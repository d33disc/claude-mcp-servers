#!/bin/bash
# Script to check if Claude Desktop is running and start it if not

# Path to the launch script
LAUNCH_SCRIPT="/Users/chrisdavis/Projects/MCP/scripts/launch-mcp-servers.sh"

# Check if Claude Desktop is already running
if ! pgrep -x "Claude" > /dev/null; then
    echo "Claude Desktop is not running. Starting with MCP servers..."
    $LAUNCH_SCRIPT
else
    echo "Claude Desktop is already running."
fi