#!/usr/bin/env python3
"""
Simple test client for the MCP server.

This script provides a straightforward way to test the MCP server
by calling basic endpoints and demonstrating tool functionality.
"""

import asyncio
import httpx
import json
import sys
from typing import Dict, Any, Optional

# Configuration
SERVER_URL = "http://localhost:8765"

async def make_request(method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Make a JSON-RPC request to the MCP server.
    
    Args:
        method: The JSON-RPC method to call
        params: Optional parameters for the method
        
    Returns:
        The JSON response from the server
        
    Raises:
        Exception: If the request fails
    """
    request_id = {
        "tools/list": 1,
        "tools/call": 2
    }.get(method, 0)
    
    request_data = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method
    }
    
    if params:
        request_data["params"] = params
    
    print(f"\n➡️ Sending request: {json.dumps(request_data, indent=2)}")
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{SERVER_URL}/jsonrpc",
            json=request_data,
            timeout=10.0
        )
        
        result = response.json()
        print(f"\n⬅️ Received response: {json.dumps(result, indent=2)}")
        return result

async def list_tools() -> None:
    """List all available tools from the server."""
    print("\n=== Listing available tools ===")
    result = await make_request("tools/list")
    
    if "result" in result:
        tools = result["result"]["tools"]
        print(f"\nFound {len(tools)} tools:")
        for tool in tools:
            print(f"  - {tool['name']}: {tool['description']}")
    else:
        print(f"Failed to list tools: {json.dumps(result, indent=2)}")

async def query_database() -> None:
    """Test the database query tool."""
    print("\n=== Testing database query ===")
    result = await make_request(
        "tools/call",
        {"name": "query_db"}
    )
    
    if "result" in result:
        print(f"\nQuery result: {result['result']['result']}")
    else:
        print(f"Failed to query database: {json.dumps(result, indent=2)}")

async def analyze_sample_data() -> None:
    """Test the data analysis tool with sample data."""
    print("\n=== Testing data analysis ===")
    sample_data = [10, 20, 30, 40, 50]
    
    result = await make_request(
        "tools/call",
        {
            "name": "analyze_data",
            "arguments": {
                "data": sample_data
            }
        }
    )
    
    if "result" in result:
        stats = result["result"]["result"]
        print(f"\nStatistics for data {sample_data}:")
        for key, value in stats.items():
            print(f"  - {key}: {value}")
    else:
        print(f"Failed to analyze data: {json.dumps(result, indent=2)}")

async def generate_sample_report() -> None:
    """Test the report generation tool with sample data."""
    print("\n=== Testing report generation ===")
    report_data = {
        "summary": "This is a sample data analysis report",
        "metrics": {
            "accuracy": 0.95,
            "precision": 0.92,
            "recall": 0.91,
            "f1_score": 0.93
        },
        "key_findings": [
            "Data shows strong correlation between X and Y",
            "Outliers detected in segment Z",
            "Performance metrics exceed baseline by 15%"
        ]
    }
    
    result = await make_request(
        "tools/call",
        {
            "name": "generate_report",
            "arguments": {
                "title": "Sample Data Analysis Report",
                "data": report_data
            }
        }
    )
    
    if "result" in result:
        report = result["result"]["result"]
        print("\nGenerated Report:")
        print(report)
    else:
        print(f"Failed to generate report: {json.dumps(result, indent=2)}")

async def validate_sample_data() -> None:
    """Test the data validation tool with sample data."""
    print("\n=== Testing data validation ===")
    
    # Test valid numeric data
    numeric_data = [10, 20, 30, 40, 50]
    result = await make_request(
        "tools/call",
        {
            "name": "validate_data",
            "arguments": {
                "data": numeric_data,
                "expected_type": "numeric"
            }
        }
    )
    
    if "result" in result:
        validation = result["result"]["result"]
        print(f"\nValidation results for numeric data:")
        print(f"  - Valid: {validation['valid']}")
        print(f"  - Valid count: {validation['valid_count']}")
        print(f"  - Invalid count: {validation['invalid_count']}")
    else:
        print(f"Failed to validate data: {json.dumps(result, indent=2)}")
    
    # Test mixed data types
    mixed_data = [10, "twenty", 30, True, 50]
    result = await make_request(
        "tools/call",
        {
            "name": "validate_data",
            "arguments": {
                "data": mixed_data,
                "expected_type": "numeric"
            }
        }
    )
    
    if "result" in result:
        validation = result["result"]["result"]
        print(f"\nValidation results for mixed data:")
        print(f"  - Valid: {validation['valid']}")
        print(f"  - Valid count: {validation['valid_count']}")
        print(f"  - Invalid count: {validation['invalid_count']}")
        
        if validation["invalid_count"] > 0:
            print(f"  - Invalid values:")
            for invalid in validation["invalid_values"]:
                print(f"    - Index {invalid['index']}: {invalid['value']} (type: {invalid['actual_type']})")
    else:
        print(f"Failed to validate data: {json.dumps(result, indent=2)}")

async def main() -> None:
    """Run all tests sequentially."""
    try:
        print(f"🚀 Testing MCP server at {SERVER_URL}")
        
        # Step 1: List available tools
        await list_tools()
        
        # Step 2: Test query_db tool
        await query_database()
        
        # Step 3: Test analyze_data tool
        await analyze_sample_data()
        
        # Step 4: Test generate_report tool
        await generate_sample_report()
        
        # Step 5: Test validate_data tool
        await validate_sample_data()
        
        print("\n✅ All tests completed!")
        
    except httpx.ConnectError:
        print(f"\n❌ Error: Could not connect to server at {SERVER_URL}")
        print("Please make sure the MCP server is running.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
