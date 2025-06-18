# MCP Scripts

## Introduction

This directory contains scripts for managing the Model Context Protocol (MCP) servers and Claude Desktop integration. MCP servers extend Claude's capabilities by providing additional tools and integrations with your local environment. These scripts help you install, configure, diagnose, and manage MCP servers for use with Claude Desktop.

## Script Descriptions

### Claude Desktop Management

- **claude-autostart.sh**: Checks if Claude Desktop is running and starts it if not, ensuring MCP servers are initialized first.
- **launch-mcp-servers.sh**: Initializes MCP servers before starting Claude Desktop, setting up the necessary environment.
- **reset-claude-config.sh**: Resets the Claude Desktop configuration to default state (no MCP servers).

### MCP Server Management

- **install-server.sh**: Installs and configures an MCP server for use with Claude Desktop.
- **list-servers.sh**: Lists all currently configured MCP servers in the Claude Desktop configuration.
- **diagnose-mcp.sh**: Diagnoses MCP server issues, generating a comprehensive report on the current state.
- **python-server-test.py**: Tests a Python-based MCP server to verify it works correctly.

### Configuration Management

- **clean-config.js**: Creates a clean Claude Desktop configuration with minimal servers (sequential-thinking and web-fetch).
- **update-claude-config.js**: Updates the Claude Desktop configuration to add or update MCP servers.
- **helper-functions.sh**: Contains shared helper functions used by other MCP scripts.

## Usage Instructions

### Installing an MCP Server

```bash
./install-server.sh <server-name> [server-package]
```

Example:
```bash
./install-server.sh web-fetch @modelcontextprotocol/server-web-fetch
```

### Starting Claude with MCP Servers

```bash
./launch-mcp-servers.sh
```

Options:
- `--dry-run`: Check configuration without launching Claude Desktop
- `--help`: Show help message

### Testing a Python MCP Server

```bash
./python-server-test.py <path-to-server-script>
```

Example:
```bash
./python-server-test.py /Users/chrisdavis/Projects/MCP/servers/my-python-server/server.py
```

### Diagnosing MCP Issues

```bash
./diagnose-mcp.sh
```

This will generate a comprehensive diagnostic report at `/Users/chrisdavis/Projects/MCP/mcp-diagnosis-YYYYMMDD-HHMMSS.txt`.

### Listing Configured Servers

```bash
./list-servers.sh
```

### Resetting Claude Configuration

```bash
./reset-claude-config.sh
```

### Updating Claude Configuration

```bash
node update-claude-config.js
```

### Creating a Clean Configuration

```bash
node clean-config.js
```

## Troubleshooting Tips

1. **Claude Desktop not connecting to MCP servers:**
   - Run `./diagnose-mcp.sh` to generate a diagnostic report
   - Check if servers are installed with `./list-servers.sh`
   - Try resetting the configuration with `./reset-claude-config.sh`
   - Reinstall problematic servers with `./install-server.sh`

2. **Errors during server installation:**
   - Make sure Node.js and npm are installed and updated
   - Check internet connectivity
   - Look for error messages in the Claude Desktop logs at `~/Library/Logs/Claude/claude-desktop.log`

3. **Claude Desktop not starting:**
   - Try the auto-start script: `./claude-autostart.sh`
   - Check disk space and system resources using `./diagnose-mcp.sh`
   - Verify Claude Desktop is properly installed

4. **Unexpected server behavior:**
   - For Python servers, use `./python-server-test.py` to verify functionality
   - Check the server logs in the diagnostic report
   - Try reinstalling the server with `./install-server.sh`

5. **Configuration issues:**
   - Create a clean configuration with `node clean-config.js`
   - Verify the configuration format with `./list-servers.sh`
   - Check for backup configurations in `/Users/chrisdavis/Projects/MCP/config/backups/`

For persistent issues, check the full diagnostic report and consider reinstalling Claude Desktop or specific MCP servers.