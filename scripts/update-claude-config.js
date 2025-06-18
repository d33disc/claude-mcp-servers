#!/usr/bin/env node

/**
 * Script to update Claude Desktop configuration file
 * Adds or updates MCP servers in the configuration
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// Path to Claude Desktop configuration
const configPath = path.join(os.homedir(), 'Library', 'Application Support', 'Claude', 'claude_desktop_config.json');

// Check if configuration file exists
if (!fs.existsSync(configPath)) {
  console.error(`❌ Configuration file not found at ${configPath}`);
  console.log('Creating default configuration file...');
  
  // Create directory if it doesn't exist
  const configDir = path.dirname(configPath);
  if (!fs.existsSync(configDir)) {
    fs.mkdirSync(configDir, { recursive: true });
  }
  
  // Create default configuration
  fs.writeFileSync(configPath, JSON.stringify({ mcpServers: {} }, null, 2));
  console.log(`✅ Created default configuration at ${configPath}`);
}

// Read configuration
let config;
try {
  const configData = fs.readFileSync(configPath, 'utf8');
  config = JSON.parse(configData);
} catch (error) {
  console.error(`❌ Error reading configuration: ${error.message}`);
  process.exit(1);
}

// Initialize mcpServers if it doesn't exist
if (!config.mcpServers) {
  config.mcpServers = {};
}

// Add filesystem MCP server
config.mcpServers.filesystem = {
  env: {},
  command: 'npx',
  args: [
    '-y',
    '@modelcontextprotocol/server-filesystem',
    os.homedir() // Use home directory as workspace
  ]
};

// Check for desktop-commander npm package
try {
  const commandExists = require('child_process').execSync('npm list -g @modelcontextprotocol/server-desktop-commander || npm list -g desktop-commander-mcp || echo "not installed"').toString();
  
  if (!commandExists.includes('not installed')) {
    // Add desktop-commander MCP server if installed
    config.mcpServers['desktop-commander'] = {
      env: {},
      command: 'npx',
      args: [
        '-y',
        '@modelcontextprotocol/server-desktop-commander'
      ]
    };
    console.log('✅ Added desktop-commander MCP server');
  }
} catch (error) {
  console.log('ℹ️ Desktop Commander not found, skipping');
}

// Write updated configuration
try {
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
  console.log(`✅ Updated configuration at ${configPath}`);
  console.log('ℹ️ Added filesystem MCP server');
  console.log('ℹ️ Please restart Claude Desktop to apply changes');
} catch (error) {
  console.error(`❌ Error writing configuration: ${error.message}`);
  process.exit(1);
}