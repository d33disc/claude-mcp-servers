#!/usr/bin/env python3
"""
Test utility for Python-based MCP servers
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

def send_message(proc, message):
    """Send a JSON-RPC message to the MCP server"""
    json_str = json.dumps(message)
    length = len(json_str)
    proc.stdin.write(f"Content-Length: {length}\r\n\r\n{json_str}")
    proc.stdin.flush()

def read_message(proc):
    """Read a JSON-RPC message from the MCP server"""
    header = proc.stdout.readline().decode('utf-8').strip()
    if not header.startswith("Content-Length: "):
        return None
    
    length = int(header.replace("Content-Length: ", ""))
    proc.stdout.readline()  # Skip empty line
    content = proc.stdout.read(length).decode('utf-8')
    return json.loads(content)

def test_server(server_path):
    """Test a Python MCP server"""
    try:
        proc = subprocess.Popen(
            [sys.executable, server_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=False,
            bufsize=0
        )
        
        # Test the server by sending a tools/list request
        send_message(proc, {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list"
        })
        
        response = read_message(proc)
        if response and "result" in response and "tools" in response["result"]:
            print(f"✅ Server responded successfully with {len(response['result']['tools'])} tools:")
            for tool in response["result"]["tools"]:
                print(f"  - {tool['name']}: {tool.get('description', 'No description')}")
            return True
        else:
            print("❌ Server response invalid or missing tools")
            print(f"Response: {response}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing server: {e}")
        return False
    finally:
        proc.terminate()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test a Python MCP server")
    parser.add_argument("server_path", help="Path to the Python MCP server script")
    args = parser.parse_args()
    
    server_path = Path(args.server_path).resolve()
    if not server_path.exists():
        print(f"❌ Server not found at {server_path}")
        sys.exit(1)
        
    print(f"🧪 Testing MCP server at {server_path}")
    if test_server(server_path):
        print("✅ Server test passed")
        sys.exit(0)
    else:
        print("❌ Server test failed")
        sys.exit(1)