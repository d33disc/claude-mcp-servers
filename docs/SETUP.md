# MCP Server Setup Guide

This guide provides instructions for setting up MCP servers for use with Claude Desktop and Claude Code.

## Prerequisites

- Node.js 16 or higher
- Python 3.9 or higher (for Python-based servers)
- Claude Desktop application
- Claude Code CLI (optional)

## Installation Methods

### Method 1: Using the Install Script

The simplest way to install an MCP server is using the provided script:

```bash
# Make the script executable
chmod +x ~/Projects/MCP/scripts/install-server.sh

# Install a server (e.g., web-fetch)
~/Projects/MCP/scripts/install-server.sh web-fetch
```

### Method 2: Manual Installation

For more control, you can manually install and configure MCP servers:

1. Install the server package:
   ```bash
   npm install -g @modelcontextprotocol/server-name
   ```

2. Update Claude Desktop configuration at `~/Library/Application Support/Claude/claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "server-name": {
         "env": {},
         "command": "npx",
         "args": [
           "-y",
           "@modelcontextprotocol/server-name"
         ]
       }
     }
   }
   ```

3. Restart Claude Desktop to apply changes

### Method 3: Using Claude Desktop's MCP Installer

You can also use Claude Desktop's built-in MCP installer by asking:

```
"Install the MCP server named mcp-server-name"
```

## Testing MCP Servers

### Testing a Python MCP Server

```bash
python ~/Projects/MCP/scripts/python-server-test.py /path/to/server.py
```

### Testing an npm-based MCP Server

```bash
# Installed globally
npx @modelcontextprotocol/server-name --debug

# Local server file
node /path/to/server.js --debug
```

## Troubleshooting

If you encounter issues:

1. **Verify Installation**:
   ```bash
   # For npm packages
   npm list -g @modelcontextprotocol/server-name
   
   # For Python packages
   pip list | grep mcp
   ```

2. **Check Configuration**:
   ```bash
   cat "$HOME/Library/Application Support/Claude/claude_desktop_config.json"
   ```

3. **Restart Applications**:
   Close and reopen Claude Desktop and/or Claude Code

4. **Enable Debug Mode**:
   Most servers support a `--debug` flag for verbose logging

5. **Check Logs**:
   Claude Desktop logs can be found in `~/Library/Logs/Claude/`