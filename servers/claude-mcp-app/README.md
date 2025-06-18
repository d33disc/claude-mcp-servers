# Claude MCP App

A Model-Controller-Presenter (MCP) server for Claude integration that provides data analysis, database querying, and report generation functionality.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Available Tools](#available-tools)
- [Debugging Guide](#debugging-guide)
- [Development and Testing](#development-and-testing)
- [Configuration Options](#configuration-options)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Overview

This application provides a MCP server that integrates with Claude for advanced data analysis capabilities. The server offers various tools for database querying, data analysis, report generation, and data validation, all accessible via JSON-RPC calls.

Key features:
- Database querying with robust error handling
- Statistical analysis of numeric data
- Markdown report generation
- Data validation against expected types
- Comprehensive logging
- Simple test client for development

## Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager
- Bash (for running the setup and server scripts)

### Setup

1. Clone this repository:
   ```
   git clone <repository-url>
   cd claude-mcp-app
   ```

2. Run the setup script to create a virtual environment and install dependencies:
   ```
   chmod +x setup.sh
   ./setup.sh
   ```

   The setup script will:
   - Create a Python virtual environment
   - Install required packages from requirements.txt
   - Verify installation of the MCP package

## Usage

### Starting the Server

Run the server using the provided script:

```
./run_server.sh
```

By default, the server runs on `0.0.0.0:8765`. To customize:

```
./run_server.sh --host=127.0.0.1 --port=9000 --debug
```

The server will start and be ready to receive JSON-RPC requests.

### Using the Test Client

A simple test client is included to verify server functionality:

```
python simple_test.py
```

This runs through all available tools with sample data, demonstrating how to make requests to the server.

## Available Tools

The server provides the following tools:

1. **query_db**: Execute a query against the database
   - Takes no arguments
   - Returns query results as a string

2. **analyze_data**: Perform statistical analysis on numeric data
   - Arguments: `data` (list of numbers)
   - Returns statistics (mean, median, standard deviation, min, max, count)

3. **generate_report**: Create a markdown-formatted report
   - Arguments: `title` (string), `data` (dictionary)
   - Returns a markdown-formatted string

4. **validate_data**: Validate data against expected types
   - Arguments: `data` (list), `expected_type` (string)
   - Returns validation results (valid, valid_count, invalid_count, invalid_values)

## Debugging Guide

### Enabling Debug Mode

For verbose logging:

```
./run_server.sh --debug
```

Debug mode will show detailed request and response information, stack traces, and additional logs useful for troubleshooting.

### Common Error Scenarios

#### 1. Connection Refused

**Symptom**: `Connection refused` error when trying to connect to the server.

**Causes**:
- Server isn't running
- Server is running on a different host/port
- Firewall blocking the connection

**Solution**:
- Verify server is running with `ps aux | grep mcp`
- Check configured host/port (default: 0.0.0.0:8765)
- Try connecting to localhost instead of 0.0.0.0

#### 2. Import Errors

**Symptom**: Error messages like `ModuleNotFoundError: No module named 'mcp'`

**Causes**:
- Virtual environment not activated
- MCP package not installed
- Incorrect Python version

**Solution**:
- Activate the virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`
- Verify Python version: `python --version` (should be 3.9+)

#### 3. Database Connection Issues

**Symptom**: Error when calling `query_db` tool

**Causes**:
- Database initialization failure
- Missing database configuration
- Network issues (for remote databases)

**Solution**:
- Check server logs for database connection errors
- Verify database configuration (in production environments)
- For the mock database, ensure `fake_database.py` is in the correct location

#### 4. Data Analysis Errors

**Symptom**: Errors when calling `analyze_data` tool

**Causes**:
- Invalid data types provided (non-numeric)
- Empty data lists
- Missing required arguments

**Solution**:
- Ensure input data consists only of numeric values
- Check that data list is not empty
- Verify all required arguments are provided in the request

#### 5. Report Generation Errors

**Symptom**: Errors when calling `generate_report` tool

**Causes**:
- Missing or invalid report title
- Empty or malformed data dictionary
- Unexpected data structure

**Solution**:
- Ensure report title is a non-empty string
- Verify data is a non-empty dictionary
- Structure data with appropriate sections and content types

### Logging and Troubleshooting

The server uses Python's logging module with the following configurations:

- **INFO level** (default): Shows server start/stop, successful operations
- **DEBUG level**: Shows detailed request/response, data processing information

Log messages include:
- Timestamp
- Logger name ('mcp_app')
- Log level
- Message content

To analyze logs for troubleshooting:

1. Enable debug mode:
   ```
   ./run_server.sh --debug
   ```

2. Redirect output to a file for analysis:
   ```
   ./run_server.sh --debug > server_log.txt 2>&1
   ```

3. Look for ERROR-level messages, which indicate issues that need attention

## Development and Testing

### Running Tests

To run the test suite:

```
python test_suite.py
```

This executes comprehensive tests for all server components, checking both success and error cases.

### Using the Simple Test Client

The `simple_test.py` script provides a straightforward way to test the server:

```
python simple_test.py
```

This script:
1. Lists all available tools
2. Tests the database query tool
3. Tests the data analysis tool with sample data
4. Tests the report generation tool with sample data
5. Tests the data validation tool with sample data

### Manual Testing with curl

You can also test the JSON-RPC API directly using curl:

```bash
# List available tools
curl -X POST -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' http://localhost:8765/jsonrpc

# Call analyze_data tool
curl -X POST -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"analyze_data","arguments":{"data":[10,20,30,40,50]}}}' http://localhost:8765/jsonrpc
```

## Configuration Options

### Server Configuration

The `run_server.sh` script accepts the following options:

- `--debug`: Enable debug logging (default: disabled)
- `--host=HOST`: Specify the host address (default: 0.0.0.0)
- `--port=PORT`: Specify the port number (default: 8765)
- `--help`: Display usage information

### Environment Variables

You can configure the server using environment variables:

- `LOG_LEVEL`: Set the logging level (default: "INFO", can be "DEBUG", "INFO", "WARNING", "ERROR")

Example:
```
LOG_LEVEL=DEBUG ./run_server.sh
```

## Troubleshooting

### Server Won't Start

**Symptom**: Server fails to start when running `run_server.sh`

**Possible solutions**:
- Check for port conflicts: `lsof -i :8765` to see if another process is using the port
- Verify virtual environment is set up correctly: `ls -la venv/`
- Check Python version: `python --version` (should be 3.9+)
- Reinstall dependencies: `pip install -r requirements.txt`

### Client Can't Connect

**Symptom**: `simple_test.py` or other clients can't connect to the server

**Possible solutions**:
- Verify server is running: `ps aux | grep mcp`
- Check server host/port configuration
- Ensure no firewall rules are blocking connections
- Try using `localhost` or `127.0.0.1` instead of `0.0.0.0`

### Tool Execution Failures

**Symptom**: Error when calling specific tools

**Possible solutions**:
- Check server logs for specific error messages
- Verify input parameters match the expected format
- Ensure all required arguments are provided
- For data validation issues, check input data types

### Integration with Claude Desktop

**Symptom**: Claude Desktop not connecting to MCP server

**Possible solutions**:
- Ensure server is running and accessible
- Verify Claude Desktop is configured to use the correct server URL
- Check that the MCP server definition is properly set up in Claude Desktop
- Look for networking issues that might prevent communication

## Contributing

Contributions to this project are welcome! To contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make your changes
4. Submit a pull request

Please ensure your code follows the existing style and includes appropriate tests.

## License

[Include license information here]
