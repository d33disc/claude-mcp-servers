#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Display helper message for script usage
function show_usage() {
    echo "Usage: ./run_server.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --debug        Enable debug logging"
    echo "  --host=HOST    Specify the host address (default: 0.0.0.0)"
    echo "  --port=PORT    Specify the port number (default: 8765)"
    echo "  --help         Display this help message"
    echo ""
}

# Default configuration
DEBUG=false
HOST="0.0.0.0"
PORT=8765
APP_MODULE="fixed_app:mcp"

# Parse command-line arguments
for arg in "$@"; do
    case $arg in
        --debug)
            DEBUG=true
            shift
            ;;
        --host=*)
            HOST="${arg#*=}"
            shift
            ;;
        --port=*)
            PORT="${arg#*=}"
            shift
            ;;
        --help)
            show_usage
            exit 0
            ;;
        *)
            echo "Unknown option: $arg"
            show_usage
            exit 1
            ;;
    esac
done

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Set logging level based on debug flag
if [ "$DEBUG" = true ]; then
    export LOG_LEVEL="DEBUG"
    echo "Debug logging enabled"
else
    export LOG_LEVEL="INFO"
fi

# Print server information
echo "Starting MCP server with the following configuration:"
echo "- Host: $HOST"
echo "- Port: $PORT"
echo "- Module: $APP_MODULE"
echo "- Log level: $LOG_LEVEL"
echo ""
echo "Note: Press Ctrl+C to stop the server"
echo ""

# Run the MCP server with specified configuration
python -m mcp.server dev $APP_MODULE --host $HOST --port $PORT
