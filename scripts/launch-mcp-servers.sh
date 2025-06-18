#!/bin/bash
# Script to initialize MCP servers before starting Claude Desktop

set -e

WORKSPACE_DIR="/Users/chrisdavis/code/mcp-workspace"
CONFIG_SCRIPT="${WORKSPACE_DIR}/scripts/manager.py"

# Check if workspace exists
if [ ! -d "$WORKSPACE_DIR" ]; then
    echo "❌ Error: MCP workspace not found at $WORKSPACE_DIR"
    echo "Please clone the repository or create the directory"
    exit 1
fi

# Check if Python script exists
if [ ! -f "$CONFIG_SCRIPT" ]; then
    echo "❌ Error: Configuration script not found at $CONFIG_SCRIPT"
    exit 1
fi

# Navigate to workspace directory
cd "$WORKSPACE_DIR"

# Ensure dependencies are installed
echo "📦 Checking dependencies..."
make setup

# Generate Claude configuration
echo "🔧 Generating Claude configuration..."
make config

# Show status
echo "📊 Current MCP server status:"
make status

# Launch Claude Desktop
echo "🚀 Starting Claude Desktop..."
open -a "Claude"

echo "✅ Done! Claude Desktop should be starting with MCP servers configured."
echo "If you encounter issues, run:"
echo "  cd $WORKSPACE_DIR && make verify"