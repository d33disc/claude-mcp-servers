#!/bin/bash
# Shared helper functions for MCP scripts

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to handle errors
handle_error() {
    echo "❌ Error: $1"
    exit 1
}

# Function to check if Claude Desktop is installed
check_claude_installed() {
    CLAUDE_APP="$1"
    
    # Check different ways depending on OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS - try AppleScript
        if command_exists osascript; then
            if osascript -e "exists application \"$CLAUDE_APP\"" >/dev/null 2>&1; then
                return 0
            fi
        fi
        
        # Check Applications directories
        if [ -d "/Applications/Claude.app" ] || [ -d "$HOME/Applications/Claude.app" ]; then
            return 0
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux - check if in PATH
        if command_exists "$CLAUDE_APP"; then
            return 0
        fi
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        # Windows - just check if command exists
        if command_exists "$CLAUDE_APP"; then
            return 0
        fi
    fi
    
    # Not found
    return 1
}

# Function to check if Claude Desktop is running
is_claude_running() {
    CLAUDE_APP="$1"
    
    # Different ways to check depending on OS
    if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # macOS/Linux - use pgrep
        if command_exists pgrep; then
            if pgrep -x "$CLAUDE_APP" > /dev/null; then
                return 0
            fi
        else
            # Fallback to ps and grep
            if ps aux | grep -v grep | grep -q "$CLAUDE_APP"; then
                return 0
            fi
        fi
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        # Windows - use tasklist
        if command_exists tasklist; then
            if tasklist | grep -i "$CLAUDE_APP" > /dev/null; then
                return 0
            fi
        fi
    fi
    
    # Not running
    return 1
}

# Function to launch Claude Desktop
launch_claude() {
    CLAUDE_APP="$1"
    
    echo "🚀 Starting Claude Desktop..."
    
    # Different launch methods depending on OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        open -a "$CLAUDE_APP" || return 1
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        "$CLAUDE_APP" > /dev/null 2>&1 & disown || return 1
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        # Windows
        start "$CLAUDE_APP" > /dev/null 2>&1 || return 1
    else
        # Unknown OS
        return 1
    fi
    
    return 0
}

# Function to create a backup of a file
backup_file() {
    SOURCE="$1"
    BACKUP_DIR="$2"
    
    if [ ! -f "$SOURCE" ]; then
        return 1
    fi
    
    # Create backup directory if it doesn't exist
    mkdir -p "$BACKUP_DIR"
    
    # Create backup with timestamp
    TIMESTAMP=$(date +%Y%m%d-%H%M%S)
    FILENAME=$(basename "$SOURCE")
    cp "$SOURCE" "$BACKUP_DIR/${FILENAME}-${TIMESTAMP}.bak" || return 1
    
    return 0
}