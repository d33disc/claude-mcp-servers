# MCP Servers for Claude

This repository serves as the central hub for all Model Context Protocol (MCP) servers used with Claude Desktop and Claude Code applications.

## Structure

- `servers/` - MCP server implementations 
- `config/` - Configuration files and backups
- `docs/` - Documentation for each server
- `scripts/` - Utility scripts for installation and management

## Available MCP Servers

| Server Name | Description | Compatible With |
|-------------|-------------|-----------------|
| sequential-thinking | Structured step-by-step reasoning | Desktop & Code |
| web-fetch | Access online information | Desktop & Code |
| vector-store | Vector database for embeddings | Desktop & Code |
| code-interpreter | Execute code in various languages | Desktop & Code |
| claude-mcp-app | Data analysis & reporting | Code |
| mcp-installer | Tool to install additional servers | Desktop |

## Installation & Setup

See the detailed instructions in the `docs/` directory for each server's installation and configuration process.

## Usage

Each MCP server extends Claude's capabilities in specific ways:

- **Sequential Thinking**: Use `/sequential-thinking` in your prompt for complex reasoning
- **Web Fetch**: Request information from the web
- **Vector Store**: Store and retrieve embeddings for RAG applications
- **Code Interpreter**: Execute code in various languages

## Development

To add new MCP servers:

1. Create a new directory in `servers/`
2. Follow the MCP server development guidelines
3. Add appropriate tests
4. Update the configuration in `config/`
5. Document the server in `docs/`

## Tests

Each server includes its own test suite. Run tests with:

```bash
cd servers/[server-name]
npm test  # For JavaScript servers
python -m unittest  # For Python servers
```