#!/usr/bin/env node

/**
 * Script to create a clean Claude Desktop configuration file
 * Use this when experiencing issues with MCP servers
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// Path to Claude Desktop configuration
const configPath = path.join(os.homedir(), 'Library', 'Application Support', 'Claude', 'claude_desktop_config.json');
const backupDir = path.join(os.homedir(), 'Projects', 'MCP', 'config', 'backups');

// Create backup directory if it doesn't exist
if (!fs.existsSync(backupDir)) {
  fs.mkdirSync(backupDir, { recursive: true });
}

// Backup current config if it exists
if (fs.existsSync(configPath)) {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const backupPath = path.join(backupDir, `claude_desktop_config-${timestamp}.json`);
  fs.copyFileSync(configPath, backupPath);
  console.log(`✅ Created backup at ${backupPath}`);
}

// Create directory if it doesn't exist
const configDir = path.dirname(configPath);
if (!fs.existsSync(configDir)) {
  fs.mkdirSync(configDir, { recursive: true });
}

// Create clean configuration with minimal servers
const cleanConfig = {
  mcpServers: {
    "sequential-thinking": {
      "env": {},
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-sequential-thinking"
      ]
    },
    "web-fetch": {
      "env": {},
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-web-fetch"
      ]
    }
  }
};

// Write clean configuration
fs.writeFileSync(configPath, JSON.stringify(cleanConfig, null, 2));
console.log(`✅ Created clean configuration at ${configPath}`);
console.log('ℹ️ Only sequential-thinking and web-fetch servers are enabled');
console.log('ℹ️ Please restart Claude Desktop to apply changes');