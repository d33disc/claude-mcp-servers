# Complete Guide to Setting Up an MCP Server for Claude Desktop

This guide provides comprehensive, step-by-step instructions for setting up a Model Context Protocol (MCP) server that integrates with Claude Desktop.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Server](#running-the-server)
- [Testing the Integration](#testing-the-integration)
- [Troubleshooting](#troubleshooting)
- [Extending the Server](#extending-the-server)

## Prerequisites

Before beginning, ensure you have:

- Python 3.9 or higher installed
- Claude Desktop application installed
- Basic knowledge of terminal/command line usage
- Administrative access to your machine (for installing packages)

## Installation

### 1. Install the `uv` Package Manager

The MCP Python SDK recommends using `uv` for package management. Install it with Homebrew (on macOS):

```bash
brew install uv
```

For other platforms, follow the [official uv installation guide](https://github.com/astral-sh/uv).

### 2. Set Up Your Project Directory

Create a directory for your MCP server project:

```bash
mkdir -p ~/code/mcp-installer
cd ~/code/mcp-installer
```

### 3. Create and Activate a Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

You should now see `(venv)` at the beginning of your terminal prompt, indicating the virtual environment is active.

### 4. Install the MCP Python SDK

Install the MCP Python SDK directly from GitHub:

```bash
pip install git+https://github.com/modelcontextprotocol/python-sdk.git
```

Alternatively, using `uv`:

```bash
uv pip install git+https://github.com/modelcontextprotocol/python-sdk.git
```

## Configuration

### 1. Create the MCP Server Script

Create a file named `fast_mcp_server.py` with the following content:

```python
#!/usr/bin/env python3
"""
Simple MCP server using the FastMCP API from the Python SDK
"""

from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("TestServer")

# Add a simple echo tool
@mcp.tool()
def echo(message: str) -> str:
    """Echo back a message."""
    return message

# Add a simple addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    # The run method is the proper way to start a FastMCP server
    mcp.run(transport="stdio")
```

This script creates an MCP server with three capabilities:
- An `echo` tool that repeats back any message
- An `add` tool that performs addition
- A `greeting` resource that provides personalized greetings

### 2. Configure Claude Desktop

Create a configuration file for Claude Desktop:

```bash
mkdir -p ~/Library/Application\ Support/Claude/
```

Create the file `~/Library/Application\ Support/Claude/claude_desktop_config.json` with the following content:

```json
{
  "mcpServers": {
    "testserver": {
      "command": "python3",
      "args": [
        "/Users/chrisdavis/code/mcp-installer/fast_mcp_server.py"
      ]
    }
  }
}
```

Replace `YOUR_USERNAME` with your actual username.

## Running the Server

### 1. Ensure Your Virtual Environment is Activated

If you've started a new terminal session, don't forget to activate your virtual environment:

```bash
cd ~/code/mcp-installer
source venv/bin/activate
```

### 2. Start the MCP Server

Run the server script:

```bash
python fast_mcp_server.py
```

You should see no output initially - this is normal, as the server is waiting for connections from Claude Desktop.

**Important:** Keep this terminal window open and running while using Claude Desktop.

### 3. Start or Restart Claude Desktop

If Claude Desktop is already running, quit the application and start it again. This is necessary for Claude Desktop to recognize and connect to your MCP server.

## Testing the Integration

Once Claude Desktop has restarted, you can test the integration by asking Claude to use your server's tools:

1. **Test the Echo Tool:**
   Ask Claude: "Can you use the echo tool to repeat 'Hello, MCP server is working!'"

2. **Test the Add Tool:**
   Ask Claude: "Can you use the add tool to calculate 42 + 58"

3. **Test the Greeting Resource:**
   Ask Claude: "Can you access the greeting resource with my name?"

If Claude successfully performs these actions, your MCP server is correctly set up and integrated!

## Troubleshooting

### Common Issues

#### "No module named 'mcp'"
- Ensure the virtual environment is activated
- Verify the MCP SDK is installed: `pip list | grep mcp`

#### Claude Can't Find the Server
- Check the configuration file path and content
- Ensure the path to your script in the configuration file is correct
- Verify Claude Desktop has been restarted

#### Server Crashes on Startup
- Check for Python version compatibility (3.9+)
- Look for error messages in the terminal
- Verify the server script syntax

#### Claude Desktop Can't Connect to the Server
- Make sure the server is running in a terminal
- Check the configuration file for correct paths
- Verify the script has execute permissions: `chmod +x fast_mcp_server.py`

## Extending the Server

You can extend your MCP server by adding more tools, resources, or prompts:

### Adding a New Tool

```python
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b
```

### Adding a New Resource

```python
@mcp.resource("data://current-time")
def get_current_time() -> str:
    """Get the current time."""
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
```

### Adding a Prompt Template

```python
@mcp.prompt()
def analyze_text(text: str) -> str:
    """Create an analysis prompt for the given text."""
    return f"""Please analyze the following text:

{text}

Include information about:
1. Main themes
2. Tone and style
3. Key insights
"""
```

## Additional Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [Python SDK GitHub Repository](https://github.com/modelcontextprotocol/python-sdk)
- [Claude Desktop Support](https://support.anthropic.com/)
