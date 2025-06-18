#!/bin/bash
# List all configured MCP servers

CONFIG_FILE="$HOME/Library/Application Support/Claude/claude_desktop_config.json"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ Claude Desktop configuration not found at $CONFIG_FILE"
    exit 1
fi

echo "📋 MCP Servers configured in Claude Desktop:"
echo

node -e "
const fs = require('fs');
const configPath = '$CONFIG_FILE';
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

if (!config.mcpServers || Object.keys(config.mcpServers).length === 0) {
    console.log('No MCP servers configured');
    process.exit(0);
}

console.log('| Server Name | Command | Arguments |');
console.log('|-------------|---------|-----------|');

for (const [name, server] of Object.entries(config.mcpServers)) {
    const command = server.command || 'N/A';
    const args = server.args ? server.args.join(' ') : 'N/A';
    console.log(\`| \${name} | \${command} | \${args} |\`);
}
"

echo
echo "ℹ️ Installed npm MCP packages:"
npm list -g | grep modelcontextprotocol