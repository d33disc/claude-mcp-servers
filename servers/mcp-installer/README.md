# MCP Server for Claude Desktop

A simple Model Context Protocol (MCP) server implementation that integrates with Claude Desktop, providing basic tools and resources.

## Features

- **Echo Tool**: Repeats back a message
- **Add Tool**: Performs addition of two numbers
- **Greeting Resource**: Provides personalized greetings

## Requirements

- Python 3.9+
- Claude Desktop application
- `uv` package manager (recommended) or `pip`

## Quick Start

```bash
# Clone this repository
git clone https://github.com/yourusername/mcp-installer.git
cd mcp-installer

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install git+https://github.com/modelcontextprotocol/python-sdk.git

# Run the MCP server
python fast_mcp_server.py
```

Then restart Claude Desktop to connect to the server.

## Detailed Setup

See [HOWTO.md](HOWTO.md) for step-by-step instructions.

## Project Structure

```
mcp-installer/
├── fast_mcp_server.py     # Main MCP server implementation
├── claude_desktop_config.json  # Configuration for Claude Desktop
├── setup.sh               # Setup script for configuration
├── README.md              # This file
└── HOWTO.md               # Detailed instructions
```

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
