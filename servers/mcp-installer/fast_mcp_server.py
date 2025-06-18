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
