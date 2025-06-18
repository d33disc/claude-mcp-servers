# Desktop Commander Integration

This document provides information about Desktop Commander MCP, an extension for Claude Desktop that enables file system and terminal interactions.

## What is Desktop Commander?

Desktop Commander is an open-source tool that enhances Claude Desktop by allowing it to:

- Access and process local files
- Execute terminal commands
- Work directly with your development environment
- Automate tasks and workflows

Desktop Commander effectively transforms Claude from a conversational AI into a comprehensive development assistant capable of working directly with your computer's file system and processes.

## Installation

### Option 1: NPX Installation

```bash
npx desktop-commander-mcp
```

### Option 2: Global Installation

```bash
npm install -g desktop-commander-mcp
# or
npm install -g @modelcontextprotocol/server-desktop-commander
```

### Option 3: Automatic Configuration

Run the update script from this repository:

```bash
cd /Users/chrisdavis/Projects/MCP
node scripts/update-claude-config.js
```

This script will:
1. Check if Desktop Commander is installed
2. If found, add it to your Claude Desktop configuration
3. Also add the filesystem MCP server for basic file access

## Features

Desktop Commander provides several powerful capabilities:

- **File System Access**: Read, write, and manage files
- **Terminal Command Execution**: Run any terminal command
- **Environment Integration**: Work within your development environment
- **Task Automation**: Automate repetitive tasks
- **Cross-Platform Support**: Works on Windows, macOS, and Linux

## Usage

After installation and configuration:

1. Restart Claude Desktop
2. Start a new conversation
3. Ask Claude to:
   - Read or modify files
   - Execute terminal commands
   - Help with development tasks

## Benefits

Desktop Commander turns Claude into a versatile development assistant for:

- Software engineering
- DevOps
- Technical writing
- System administration
- Data analysis

## More Information

For more details and the latest updates, visit the [Desktop Commander website](https://desktopcommander.app/).

## License

Desktop Commander is free for personal use, with a licensing fee for companies meeting certain revenue thresholds. See the website for details.