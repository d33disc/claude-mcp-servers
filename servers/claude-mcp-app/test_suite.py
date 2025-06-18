#!/usr/bin/env python3
"""
Comprehensive test suite for the MCP server application.

This script performs a series of tests to verify the functionality of the MCP server,
including connection, tool availability, and tool functionality. It can either connect
to an already running server or start its own server instance for testing.

Usage:
    ./test_suite.py [--start-server]

Options:
    --start-server  Start a new MCP server instance for testing
"""

import asyncio
import httpx
import json
import sys
import time
import subprocess
import signal
import os
from typing import Dict, Any, List, Optional, Tuple, Union

# Configuration
SERVER_URL = "http://localhost:8765"
SERVER_START_TIMEOUT = 5  # seconds to wait for server to start

# ANSI color codes for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"

def print_header(message: str) -> None:
    """
    Print a formatted header message.
    
    Args:
        message: The header message to display
    """
    print(f"\n{BOLD}{message}{RESET}")

def print_success(message: str) -> None:
    """
    Print a success message with green color.
    
    Args:
        message: The success message to display
    """
    print(f"{GREEN}✅ {message}{RESET}")

def print_error(message: str) -> None:
    """
    Print an error message with red color.
    
    Args:
        message: The error message to display
    """
    print(f"{RED}❌ {message}{RESET}")

def print_warning(message: str) -> None:
    """
    Print a warning message with yellow color.
    
    Args:
        message: The warning message to display
    """
    print(f"{YELLOW}⚠️ {message}{RESET}")

async def wait_for_server(url: str, timeout: int = 5) -> bool:
    """
    Wait for the server to become available by attempting to connect.
    
    Args:
        url: The server URL to check
        timeout: Maximum time to wait in seconds
        
    Returns:
        True if server is available, False otherwise
    """
    print(f"Waiting for server at {url} (timeout: {timeout}s)...")
    end_time = time.time() + timeout
    
    while time.time() < end_time:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{url}/jsonrpc",
                    json={
                        "jsonrpc": "2.0",
                        "id": 0,
                        "method": "tools/list"
                    },
                    timeout=1.0
                )
                if response.status_code == 200:
                    print_success(f"Server is available at {url}")
                    return True
        except (httpx.ConnectError, httpx.TimeoutException):
            pass
        
        # Wait a short time before retrying
        await asyncio.sleep(0.5)
    
    print_error(f"Server not available at {url} after {timeout}s")
    return False

async def list_tools() -> List[Dict[str, Any]]:
    """
    List all available tools from the server.
    
    Returns:
        List of tool definitions
    """
    print_header("Testing tools/list endpoint")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SERVER_URL}/jsonrpc",
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/list"
                }
            )
            result = response.json()
            
            if "result" in result:
                tools = result["result"]["tools"]
                print_success(f"Found {len(tools)} tools:")
                for tool in tools:
                    print(f"  - {tool['name']}: {tool['description']}")
                return tools
            else:
                print_error(f"Failed to list tools: {json.dumps(result, indent=2)}")
                return []
    except Exception as e:
        print_error(f"Error listing tools: {e}")
        return []

async def test_query_db() -> bool:
    """
    Test the database query tool.
    
    Returns:
        True if test passed, False otherwise
    """
    print_header("Testing query_db tool")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SERVER_URL}/jsonrpc",
                json={
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/call",
                    "params": {
                        "name": "query_db"
                    }
                }
            )
            result = response.json()
            
            if "result" in result:
                print_success(f"Query result: {result['result']['result']}")
                return True
            else:
                print_error(f"Failed to query database: {json.dumps(result, indent=2)}")
                return False
    except Exception as e:
        print_error(f"Error querying database: {e}")
        return False

async def test_analyze_data() -> bool:
    """
    Test the data analysis tool with valid and invalid inputs.
    
    Returns:
        True if all tests passed, False otherwise
    """
    print_header("Testing analyze_data tool")
    all_passed = True
    
    # Test cases with expected outcomes
    test_cases = [
        {
            "name": "Valid numeric data",
            "data": [10, 20, 30, 40, 50],
            "should_succeed": True
        },
        {
            "name": "Empty data list",
            "data": [],
            "should_succeed": False
        },
        {
            "name": "Mixed data types",
            "data": [10, "20", 30, 40, 50],
            "should_succeed": False
        }
    ]
    
    for test_case in test_cases:
        try:
            print(f"\nRunning test case: {test_case['name']}")
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{SERVER_URL}/jsonrpc",
                    json={
                        "jsonrpc": "2.0",
                        "id": 3,
                        "method": "tools/call",
                        "params": {
                            "name": "analyze_data",
                            "arguments": {
                                "data": test_case["data"]
                            }
                        }
                    }
                )
                result = response.json()
                
                if "result" in result and test_case["should_succeed"]:
                    stats = result["result"]["result"]
                    print_success(f"Analysis completed successfully: {json.dumps(stats, indent=2)}")
                elif "error" in result and not test_case["should_succeed"]:
                    print_success(f"Expected failure occurred: {result['error']['message']}")
                elif "result" in result and not test_case["should_succeed"]:
                    print_error(f"Test should have failed but succeeded: {json.dumps(result, indent=2)}")
                    all_passed = False
                elif "error" in result and test_case["should_succeed"]:
                    print_error(f"Test should have succeeded but failed: {result['error']['message']}")
                    all_passed = False
                else:
                    print_error(f"Unexpected response: {json.dumps(result, indent=2)}")
                    all_passed = False
        except Exception as e:
            print_error(f"Error in test case '{test_case['name']}': {e}")
            all_passed = False
    
    return all_passed

async def test_generate_report() -> bool:
    """
    Test the report generation tool.
    
    Returns:
        True if test passed, False otherwise
    """
    print_header("Testing generate_report tool")
    try:
        report_data = {
            "summary": "This is a test report",
            "metrics": {
                "accuracy": 0.95,
                "precision": 0.92,
                "recall": 0.91
            },
            "conclusions": ["Point 1", "Point 2", "Point 3"]
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SERVER_URL}/jsonrpc",
                json={
                    "jsonrpc": "2.0",
                    "id": 4,
                    "method": "tools/call",
                    "params": {
                        "name": "generate_report",
                        "arguments": {
                            "title": "Test Report",
                            "data": report_data
                        }
                    }
                }
            )
            result = response.json()
            
            if "result" in result:
                # Only show a preview of the report for brevity
                report_lines = result["result"]["result"].split("\n")
                preview = "\n".join(report_lines[:10])
                if len(report_lines) > 10:
                    preview += "\n..."
                
                print_success("Report generated successfully")
                print(f"\nReport preview:\n{preview}")
                return True
            else:
                print_error(f"Failed to generate report: {json.dumps(result, indent=2)}")
                return False
    except Exception as e:
        print_error(f"Error generating report: {e}")
        return False

async def test_validate_data() -> bool:
    """
    Test the data validation tool.
    
    Returns:
        True if test passed, False otherwise
    """
    print_header("Testing validate_data tool")
    all_passed = True
    
    # Test cases with expected outcomes
    test_cases = [
        {
            "name": "Valid numeric data",
            "data": [10, 20, 30, 40, 50],
            "expected_type": "numeric",
            "expected_valid": True
        },
        {
            "name": "Valid string data",
            "data": ["a", "b", "c"],
            "expected_type": "string",
            "expected_valid": True
        },
        {
            "name": "Invalid mixed data",
            "data": [10, "20", 30],
            "expected_type": "numeric",
            "expected_valid": False
        }
    ]
    
    for test_case in test_cases:
        try:
            print(f"\nRunning test case: {test_case['name']}")
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{SERVER_URL}/jsonrpc",
                    json={
                        "jsonrpc": "2.0",
                        "id": 5,
                        "method": "tools/call",
                        "params": {
                            "name": "validate_data",
                            "arguments": {
                                "data": test_case["data"],
                                "expected_type": test_case["expected_type"]
                            }
                        }
                    }
                )
                result = response.json()
                
                if "result" in result:
                    validation = result["result"]["result"]
                    if validation["valid"] == test_case["expected_valid"]:
                        print_success(f"Validation produced expected result: {json.dumps(validation, indent=2)}")
                    else:
                        print_error(f"Validation result does not match expected outcome: {json.dumps(validation, indent=2)}")
                        all_passed = False
                else:
                    print_error(f"Failed to validate data: {json.dumps(result, indent=2)}")
                    all_passed = False
        except Exception as e:
            print_error(f"Error in test case '{test_case['name']}': {e}")
            all_passed = False
    
    return all_passed

async def run_tests() -> Dict[str, bool]:
    """
    Run all tests sequentially.
    
    Returns:
        Dictionary mapping test names to pass/fail status
    """
    print_header("🚀 Starting MCP server test suite")
    
    # Wait for server to be available
    if not await wait_for_server(SERVER_URL, SERVER_START_TIMEOUT):
        print_error("Cannot proceed with tests as server is not available")
        return {}
    
    # Track test results
    results = {}
    
    # Step 1: List available tools
    tools = await list_tools()
    results["list_tools"] = len(tools) > 0
    
    # Step 2: Test query_db tool
    results["query_db"] = await test_query_db()
    
    # Step 3: Test analyze_data tool
    results["analyze_data"] = await test_analyze_data()
    
    # Step 4: Test generate_report tool
    results["generate_report"] = await test_generate_report()
    
    # Step 5: Test validate_data tool
    results["validate_data"] = await test_validate_data()
    
    return results

def print_test_summary(results: Dict[str, bool]) -> bool:
    """
    Print a summary of test results.
    
    Args:
        results: Dictionary mapping test names to pass/fail status
        
    Returns:
        True if all tests passed, False otherwise
    """
    if not results:
        return False
        
    print_header("📊 Test Results Summary")
    all_passed = True
    
    for test_name, passed in results.items():
        if passed:
            print_success(f"{test_name}: PASSED")
        else:
            print_error(f"{test_name}: FAILED")
            all_passed = False
    
    if all_passed:
        print_success("\n🎉 All tests passed! The MCP server is working correctly.")
    else:
        print_error("\n❌ Some tests failed. Please check the errors above.")
    
    return all_passed

def start_server() -> Optional[subprocess.Popen]:
    """
    Start the server as a subprocess.
    
    Returns:
        Server process or None if failed
    """
    try:
        # Make the script executable
        os.chmod("/Users/chrisdavis/Desktop/claude-mcp-app/run_server.sh", 0o755)
        
        # Start the server
        print("Starting MCP server...")
        process = subprocess.Popen(
            ["/Users/chrisdavis/Desktop/claude-mcp-app/run_server.sh"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd="/Users/chrisdavis/Desktop/claude-mcp-app"
        )
        
        # Give the server a moment to start
        time.sleep(1)
        
        return process
    except Exception as e:
        print_error(f"Failed to start server: {e}")
        return None

def stop_server(process: subprocess.Popen) -> None:
    """
    Stop the server process.
    
    Args:
        process: Server process to stop
    """
    if process:
        print("Stopping MCP server...")
        process.send_signal(signal.SIGINT)
        try:
            process.wait(timeout=5)
            print_success("Server stopped cleanly")
        except subprocess.TimeoutExpired:
            print_warning("Server did not stop cleanly, forcefully terminating")
            process.kill()

if __name__ == "__main__":
    server_process = None
    try:
        # Parse command-line arguments
        start_own_server = "--start-server" in sys.argv
        
        if start_own_server:
            server_process = start_server()
            if not server_process:
                sys.exit(1)
        
        # Run tests
        test_results = asyncio.run(run_tests())
        all_passed = print_test_summary(test_results)
        
        # Exit with appropriate status code
        sys.exit(0 if all_passed else 1)
    finally:
        # Always stop the server if we started it
        if server_process:
            stop_server(server_process)
