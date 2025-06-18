# ZSH Integration for Claude Desktop

This document explains how the MCP servers for Claude Desktop have been integrated with your ZSH shell configuration.

## Available Commands

The following commands have been added to your shell:

### Claude Desktop Shortcuts

| Command | Alias | Description |
|---------|-------|-------------|
| `claude-start` | `cs` | Launches Claude Desktop with properly configured MCP servers |

### MCP Utilities

| Command | Description |
|---------|-------------|
| `mcp-status` | Shows status of all configured MCP servers |
| `mcp-list` | Lists all MCP servers in the workspace configuration |
| `mcp-verify` | Verifies your MCP workspace structure and dependencies |

## Auto-Start Feature

Your ZSH configuration now includes an auto-start feature that:

1. Checks if Claude Desktop is already running
2. If not, launches it with properly configured MCP servers
3. If already running, does nothing

This happens automatically when you open a new terminal window or tab.

### Disabling Auto-Start

If you prefer not to automatically start Claude Desktop with every terminal session:

1. Edit your `~/.zshrc` file
2. Comment out or remove this line:
   ```bash
   /Users/chrisdavis/Projects/MCP/scripts/claude-autostart.sh
   ```

## How It Works

The integration consists of three components:

1. **Aliases in `~/.zshrc`**: Provide convenient shortcuts for common commands
2. **Launch script**: Ensures MCP servers are properly configured before starting Claude Desktop
3. **Auto-start script**: Checks if Claude Desktop is running and starts it if needed

## Customization

You can customize this setup by:

1. **Adding more aliases**: Edit `~/.zshrc` to add more shortcuts
2. **Modifying auto-start behavior**: Edit the auto-start script to change conditions or add delays
3. **Adding terminal notifications**: Modify the scripts to display desktop notifications

## Troubleshooting

If you encounter issues:

1. **Check ZSH configuration**: Ensure your `~/.zshrc` has the correct paths
2. **Verify auto-start script**: Make sure it's executable (`chmod +x`)
3. **Check launch script**: Ensure it points to the correct MCP workspace
4. **Terminal output**: Look for error messages when a terminal starts

For more help, see the main [Troubleshooting Guide](TROUBLESHOOTING.md).