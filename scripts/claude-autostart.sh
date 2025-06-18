#!/bin/bash
# Script to check if Claude Desktop is running and start it if not

# Source helper functions
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
source "$SCRIPT_DIR/helper-functions.sh" || { echo "❌ Error: Could not source helper functions"; exit 1; }

# Path to the launch script
LAUNCH_SCRIPT="/Users/chrisdavis/Projects/MCP/scripts/launch-mcp-servers.sh"
CLAUDE_APP_NAME="Claude"

# Check if launch script exists
if [ ! -f "$LAUNCH_SCRIPT" ]; then
    handle_error "Launch script not found at $LAUNCH_SCRIPT"
    exit 1
fi

# Check if launch script is executable
if [ ! -x "$LAUNCH_SCRIPT" ]; then
    chmod +x "$LAUNCH_SCRIPT" || handle_error "Could not make launch script executable"
fi

# Check if Claude Desktop is installed
if ! check_claude_installed "$CLAUDE_APP_NAME"; then
    echo "⚠️ Warning: Claude Desktop application not found in standard locations."
    echo "Attempting to launch anyway..."
fi

# Check if Claude Desktop is already running
if ! is_claude_running "$CLAUDE_APP_NAME"; then
    echo "Claude Desktop is not running. Starting with MCP servers..."
    # Run in background to prevent terminal from waiting
    "$LAUNCH_SCRIPT" &
else
    echo "Claude Desktop is already running."
fi