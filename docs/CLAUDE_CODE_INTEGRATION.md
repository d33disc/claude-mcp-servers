# Claude Code Integration

This document describes how to integrate the Claude Code MCP server with Claude Desktop.

## Overview

Claude Code provides a set of tools that allow Claude to understand and manipulate code, run commands, and interact with your development environment. By adding it as an MCP server to Claude Desktop, you can enhance Claude's capabilities with coding assistance features.

## Installation

The Claude Code MCP server has been installed globally and added to your Claude Desktop configuration:

```bash
# Install globally
npm install -g @anthropic-ai/claude-code

# Add to Claude Desktop configuration
./scripts/install-server.sh claude-code @anthropic-ai/claude-code
```

## Configuration

The Claude Desktop configuration has been updated to include the Claude Code MCP server:

```json
{
  "mcpServers": {
    "claude-code": {
      "env": {},
      "command": "npx",
      "args": [
        "-y",
        "@anthropic-ai/claude-code"
      ]
    }
  }
}
```

## Features

With Claude Code integrated, you can now:

- Ask Claude to analyze code
- Get help with debugging
- Generate code examples
- Explain code functionality
- Get recommendations for code improvements

## Usage

To use Claude Code features in Claude Desktop:

1. Restart Claude Desktop to apply the configuration changes
2. Start a new conversation
3. Ask code-related questions or request code assistance

## Troubleshooting

If you encounter issues with Claude Code in Claude Desktop:

1. Verify the installation:
   ```bash
   npm list -g @anthropic-ai/claude-code
   ```

2. Check the Claude Desktop configuration:
   ```bash
   cat "$HOME/Library/Application Support/Claude/claude_desktop_config.json"
   ```

3. Look for any error messages in the Claude Desktop logs:
   ```bash
   cat "$HOME/Library/Logs/Claude/claude-desktop.log"
   ```