#!/bin/bash
# Diagnostic script for MCP servers and Claude Desktop

set -e

CONFIG_FILE="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
LOG_FILE="$HOME/Library/Logs/Claude/claude-desktop.log"
REPORT_FILE="$HOME/Projects/MCP/mcp-diagnosis-$(date +%Y%m%d-%H%M%S).txt"

echo "# MCP Server Diagnostic Report" > "$REPORT_FILE"
echo "Generated on $(date)" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Check if Claude Desktop is running
echo "## Claude Desktop Status" >> "$REPORT_FILE"
if pgrep -x "Claude" > /dev/null; then
    echo "Claude Desktop is running" >> "$REPORT_FILE"
else
    echo "Claude Desktop is NOT running" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# Check Node.js version
echo "## Node.js Version" >> "$REPORT_FILE"
node -v >> "$REPORT_FILE" 2>&1 || echo "Node.js not found" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Check npm version
echo "## npm Version" >> "$REPORT_FILE"
npm -v >> "$REPORT_FILE" 2>&1 || echo "npm not found" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# List installed MCP packages
echo "## Installed MCP Packages" >> "$REPORT_FILE"
echo "### Global Packages" >> "$REPORT_FILE"
npm list -g | grep modelcontextprotocol >> "$REPORT_FILE" 2>&1 || echo "No MCP packages found" >> "$REPORT_FILE"
npm list -g | grep wonderwhy-er >> "$REPORT_FILE" 2>&1 || echo "No Desktop Commander packages found" >> "$REPORT_FILE"
npm list -g | grep anthropic >> "$REPORT_FILE" 2>&1 || echo "No Anthropic packages found" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Check Claude Desktop configuration
echo "## Claude Desktop Configuration" >> "$REPORT_FILE"
if [ -f "$CONFIG_FILE" ]; then
    echo "Configuration file exists at $CONFIG_FILE" >> "$REPORT_FILE"
    echo "### Configured MCP Servers:" >> "$REPORT_FILE"
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
    " >> "$REPORT_FILE" 2>&1 || echo "Error parsing configuration" >> "$REPORT_FILE"
else
    echo "Configuration file NOT found at $CONFIG_FILE" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# Check for recent errors in logs
echo "## Recent Errors in Claude Desktop Logs" >> "$REPORT_FILE"
if [ -f "$LOG_FILE" ]; then
    echo "Log file exists at $LOG_FILE" >> "$REPORT_FILE"
    echo "### Last 10 error entries:" >> "$REPORT_FILE"
    grep -i error "$LOG_FILE" | tail -n 10 >> "$REPORT_FILE" 2>&1 || echo "No errors found in logs" >> "$REPORT_FILE"
else
    echo "Log file NOT found at $LOG_FILE" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# Check internet connectivity
echo "## Internet Connectivity" >> "$REPORT_FILE"
ping -c 3 anthropic.com >> "$REPORT_FILE" 2>&1 || echo "Cannot reach anthropic.com" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Check disk space
echo "## Disk Space" >> "$REPORT_FILE"
df -h | grep -E "Size|/dev/disk" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Check memory usage
echo "## Memory Usage" >> "$REPORT_FILE"
vm_stat | perl -ne '/page size of (\d+)/ and $size=$1; /Pages free: (\d+)/ and printf("Free Memory: %.2f GB\n", $1 * $size / 1048576 / 1024); /Pages active: (\d+)/ and printf("Active Memory: %.2f GB\n", $1 * $size / 1048576 / 1024);' >> "$REPORT_FILE" 2>&1
echo "" >> "$REPORT_FILE"

# Recommendations
echo "## Recommendations" >> "$REPORT_FILE"
echo "Based on the diagnostics, consider these actions:" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "1. Reset Claude Desktop configuration: \`node /Users/chrisdavis/Projects/MCP/scripts/clean-config.js\`" >> "$REPORT_FILE"
echo "2. Restart Claude Desktop" >> "$REPORT_FILE"
echo "3. Check for updates to Claude Desktop" >> "$REPORT_FILE"
echo "4. Reinstall problematic MCP servers using the install script" >> "$REPORT_FILE"
echo "5. If issues persist, try completely reinstalling Claude Desktop" >> "$REPORT_FILE"

echo "✅ Diagnostic report created at $REPORT_FILE"
echo "Please check the report for potential issues and recommendations."