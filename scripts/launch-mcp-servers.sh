#!/bin/bash
# Script to initialize MCP servers before starting Claude Desktop

# Source helper functions
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
source "$SCRIPT_DIR/helper-functions.sh" || { echo "❌ Error: Could not source helper functions"; exit 1; }

# Parse command line arguments
DRY_RUN=0
for arg in "$@"; do
    case $arg in
        --dry-run)
            DRY_RUN=1
            shift
            ;;
        --help)
            echo "Usage: $0 [--dry-run] [--help]"
            echo "  --dry-run  Check configuration without launching Claude Desktop"
            echo "  --help     Show this help message"
            exit 0
            ;;
    esac
done

# Fail on errors
set -e

# Configuration
WORKSPACE_DIR="/Users/chrisdavis/code/mcp-workspace"
CONFIG_SCRIPT="${WORKSPACE_DIR}/scripts/manager.py"
CLAUDE_APP="Claude"

# Check if workspace exists
if [ ! -d "$WORKSPACE_DIR" ]; then
    handle_error "MCP workspace not found at $WORKSPACE_DIR"
fi

# Check if Python script exists
if [ ! -f "$CONFIG_SCRIPT" ]; then
    handle_error "Configuration script not found at $CONFIG_SCRIPT"
fi

# Check if make command is available
if ! command_exists make; then
    handle_error "make command not found. Please install the required build tools."
fi

# Check if Python is available
if ! command_exists python3; then
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

# Check if Claude Desktop is installed
if ! check_claude_installed "$CLAUDE_APP"; then
    echo "⚠️ Warning: Claude Desktop application not found in standard locations."
    echo "Attempting to launch anyway..."
fi

# Launch Claude Desktop unless in dry-run mode
if [ $DRY_RUN -eq 0 ]; then
    launch_claude "$CLAUDE_APP" || handle_error "Failed to open Claude Desktop"
else
    echo "🧪 Dry run complete - Claude Desktop would be launched here"
fi

echo "✅ Done! Claude Desktop should be starting with MCP servers configured."
echo "If you encounter issues, run:"
echo "  cd $WORKSPACE_DIR && make verify"