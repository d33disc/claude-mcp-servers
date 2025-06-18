#!/bin/bash
# Reset Claude Desktop configuration to default state

set -e

CONFIG_DIR="$HOME/Library/Application Support/Claude"
CONFIG_FILE="$CONFIG_DIR/claude_desktop_config.json"
BACKUP_DIR="$HOME/Projects/MCP/config/backups"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup current config if it exists
if [ -f "$CONFIG_FILE" ]; then
    TIMESTAMP=$(date +%Y%m%d-%H%M%S)
    cp "$CONFIG_FILE" "$BACKUP_DIR/claude_desktop_config-$TIMESTAMP.json"
    echo "✅ Created backup at $BACKUP_DIR/claude_desktop_config-$TIMESTAMP.json"
fi

# Create directory if it doesn't exist
mkdir -p "$CONFIG_DIR"

# Create minimal configuration with no MCP servers
cat > "$CONFIG_FILE" << EOF
{
  "mcpServers": {}
}
EOF

echo "✅ Reset Claude Desktop configuration to default (no MCP servers)"
echo "ℹ️ To add servers back, use the install-server.sh script"
echo "ℹ️ Please restart Claude Desktop to apply changes"