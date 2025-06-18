#!/bin/bash
# Script to install and configure MCP servers for Claude

set -e

CONFIG_DIR="$HOME/Library/Application Support/Claude"
CONFIG_FILE="$CONFIG_DIR/claude_desktop_config.json"
BACKUP_DIR="$HOME/Projects/MCP/config/backups"
SERVERS_DIR="$HOME/Projects/MCP/servers"

# Check arguments
if [ $# -lt 1 ]; then
    echo "Usage: $0 <server-name> [server-package]"
    echo "Example: $0 web-fetch @modelcontextprotocol/server-web-fetch"
    exit 1
fi

SERVER_NAME=$1
SERVER_PACKAGE=${2:-"@modelcontextprotocol/server-$SERVER_NAME"}

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup current config
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
cp "$CONFIG_FILE" "$BACKUP_DIR/claude_desktop_config-$TIMESTAMP.json"
echo "✅ Created backup at $BACKUP_DIR/claude_desktop_config-$TIMESTAMP.json"

# Install server package
echo "📦 Installing $SERVER_PACKAGE..."
npm install -g "$SERVER_PACKAGE"

# Update Claude Desktop config
echo "🔧 Updating Claude Desktop configuration..."
node -e "
const fs = require('fs');
const configPath = '$CONFIG_FILE';
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

// Initialize mcpServers if it doesn't exist
if (!config.mcpServers) {
    config.mcpServers = {};
}

// Add or update server configuration
config.mcpServers['$SERVER_NAME'] = {
    env: {},
    command: 'npx',
    args: ['-y', '$SERVER_PACKAGE']
};

// Write updated config
fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
"

echo "✅ Successfully installed and configured $SERVER_NAME"
echo "ℹ️ Please restart Claude Desktop to apply changes"