#!/bin/bash
# Test script for Python-based MCP servers

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Check if server path is provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 <server-path>"
    echo "Example: $0 ../servers/mcp-installer/fast_mcp_server.py"
    exit 1
fi

SERVER_PATH="$1"
ABSOLUTE_SERVER_PATH="$(cd "$(dirname "$SERVER_PATH")" && pwd)/$(basename "$SERVER_PATH")"

# Check if the server exists
if [ ! -f "$ABSOLUTE_SERVER_PATH" ]; then
    echo "❌ Server not found at $ABSOLUTE_SERVER_PATH"
    exit 1
fi

echo "🧪 Testing Python MCP server at $ABSOLUTE_SERVER_PATH"

# Run the test using the test utility
python3 "$PROJECT_DIR/scripts/python-server-test.py" "$ABSOLUTE_SERVER_PATH"

# Check the result
if [ $? -eq 0 ]; then
    echo "✅ All tests passed successfully"
    exit 0
else
    echo "❌ Tests failed"
    exit 1
fi