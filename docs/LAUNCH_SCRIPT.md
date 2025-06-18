# MCP Launch Script Guide

This document explains the purpose and usage of the MCP launch script for initializing servers before starting Claude Desktop.

## Purpose

The `launch-mcp-servers.sh` script serves as a centralized tool for initializing your MCP server environment before launching Claude Desktop. It ensures that:

1. Your MCP workspace is properly configured
2. Claude Desktop's configuration file is up-to-date
3. All enabled MCP servers are ready to use

## How It Works

The script performs these actions in sequence:

1. Navigates to your MCP workspace directory
2. Ensures all dependencies are installed
3. Generates the Claude Desktop configuration file based on the servers defined in the workspace
4. Shows the status of configured MCP servers
5. Launches the Claude Desktop application

## Usage

Simply run the script from anywhere on your system:

```bash
/Users/chrisdavis/Projects/MCP/scripts/launch-mcp-servers.sh
```

For convenience, you can add an alias to your shell configuration:

```bash
# Add to your ~/.zshrc or ~/.bashrc
alias launch-claude="/Users/chrisdavis/Projects/MCP/scripts/launch-mcp-servers.sh"
```

Then just run:

```bash
launch-claude
```

## Troubleshooting

If you encounter issues:

1. **Check MCP workspace**: Ensure your MCP workspace at `/Users/chrisdavis/code/mcp-workspace` exists and is properly configured
2. **Verify Python script**: Make sure the configuration script is present at `/Users/chrisdavis/code/mcp-workspace/scripts/manager.py`
3. **Run workspace verification**: `cd /Users/chrisdavis/code/mcp-workspace && make verify`
4. **Examine logs**: Check for error messages in the terminal output

## Customization

If you need to modify the script:

1. **Change workspace directory**: Edit the `WORKSPACE_DIR` variable if your MCP workspace is in a different location
2. **Add additional initialization steps**: Insert commands after the configuration generation if needed
3. **Modify launch behavior**: Change the `open -a "Claude"` command if needed for your system

## Relationship to Your MCP Repository

This launch script bridges between:

1. Your centralized MCP configuration (in the workspace)
2. The consolidated MCP servers in your `/Users/chrisdavis/Projects/MCP` repository
3. Claude Desktop's configuration requirements

For full control over your MCP servers, you should maintain both the workspace and the MCP repository.