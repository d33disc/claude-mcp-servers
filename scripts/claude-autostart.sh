#!/bin/bash
# Script to check if Claude Desktop is running and start it if not

# Path to the launch script
LAUNCH_SCRIPT="/Users/chrisdavis/Projects/MCP/scripts/launch-mcp-servers.sh"
CLAUDE_APP_NAME="Claude"

# Function to handle errors
handle_error() {
    echo "❌ Error: $1"
    return 1
}

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
if ! osascript -e "exists application \"$CLAUDE_APP_NAME\"" >/dev/null 2>&1; then
    handle_error "Claude Desktop application not found. Please install it first."
    exit 1
fi

# Check if Claude Desktop is already running
if ! pgrep -x "$CLAUDE_APP_NAME" > /dev/null; then
    echo "Claude Desktop is not running. Starting with MCP servers..."
    # Run in background to prevent terminal from waiting
    "$LAUNCH_SCRIPT" &
else
    echo "Claude Desktop is already running."
fi