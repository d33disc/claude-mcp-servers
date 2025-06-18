#!/bin/bash

# Create Claude config directory if it doesn't exist
mkdir -p ~/Library/Application\ Support/Claude/

# Copy config file to the proper location
cp ~/code/mcp-installer/claude_desktop_config.json ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Make the server script executable
chmod +x ~/code/mcp-installer/fast_mcp_server.py

echo "Setup complete! You can now start your MCP server with:"
echo "python3 ~/code/mcp-installer/fast_mcp_server.py"
echo "Make sure to restart Claude Desktop to connect to your MCP server."
