#!/bin/bash
# Script to initialize MCP servers before starting Claude Desktop

# Fail on errors
set -e

# Configuration
WORKSPACE_DIR="/Users/chrisdavis/code/mcp-workspace"
CONFIG_SCRIPT="${WORKSPACE_DIR}/scripts/manager.py"
CLAUDE_APP="Claude"

# Function to handle errors
handle_error() {
    echo "❌ Error: $1"
    exit 1
}

# Check if workspace exists
if [ ! -d "$WORKSPACE_DIR" ]; then
    handle_error "MCP workspace not found at $WORKSPACE_DIR"
fi

# Check if Python script exists
if [ ! -f "$CONFIG_SCRIPT" ]; then
    handle_error "Configuration script not found at $CONFIG_SCRIPT"
fi

# Check if make command is available
if ! command -v make >/dev/null 2>&1; then
    handle_error "make command not found. Please install the required build tools."
fi

# Check if Python is available
if ! command -v python3 >/dev/null 2>&1; then
    handle_error "python3 not found. Please install Python 3."
fi

# Navigate to workspace directory
cd "$WORKSPACE_DIR" || handle_error "Failed to change directory to $WORKSPACE_DIR"

# Ensure dependencies are installed
echo "📦 Checking dependencies..."
make setup || handle_error "Failed to install dependencies"

# Generate Claude configuration
echo "🔧 Generating Claude configuration..."
make config || handle_error "Failed to generate Claude configuration"

# Show status
echo "📊 Current MCP server status:"
make status || echo "⚠️ Warning: Could not get server status, but continuing..."

# Check if Claude Desktop app exists
if ! osascript -e "exists application \"$CLAUDE_APP\"" >/dev/null 2>&1; then
    handle_error "Claude Desktop application not found. Please install it first."
fi

# Launch Claude Desktop
echo "🚀 Starting Claude Desktop..."
open -a "$CLAUDE_APP" || handle_error "Failed to open Claude Desktop"

echo "✅ Done! Claude Desktop should be starting with MCP servers configured."
echo "If you encounter issues, run:"
echo "  cd $WORKSPACE_DIR && make verify"