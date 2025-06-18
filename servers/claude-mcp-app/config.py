# config.py
"""
Configuration framework for the MCP server.

This module provides configuration management for the MCP server,
allowing customization of behavior through environment variables,
configuration files, or direct settings.
"""

import os
import json
import logging
from typing import Any, Dict, Optional, Union
from dataclasses import dataclass, field, asdict

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('config')

# Default configuration values
DEFAULT_CONFIG = {
    "server": {
        "host": "0.0.0.0",
        "port": 8765,
        "debug": False,
        "log_level": "INFO"
    },
    "database": {
        "use_mock": True,
        "connection_timeout": 5.0,
        "max_retries": 3
    },
    "analysis": {
        "default_precision": 2,
        "max_data_points": 10000
    },
    "export": {
        "output_dir": "./output",
        "default_format": "json",
        "max_file_size_mb": 100
    },
    "security": {
        "enable_authentication": False,
        "api_key_required": False
    }
}

@dataclass
class ServerConfig:
    """Server configuration settings."""
    host: str = "0.0.0.0"
    port: int = 8765
    debug: bool = False
    log_level: str = "INFO"

@dataclass
class DatabaseConfig:
    """Database configuration settings."""
    use_mock: bool = True
    connection_timeout: float = 5.0
    max_retries: int = 3

@dataclass
class AnalysisConfig:
    """Data analysis configuration settings."""
    default_precision: int = 2
    max_data_points: int = 10000

@dataclass
class ExportConfig:
    """Export functionality configuration settings."""
    output_dir: str = "./output"
    default_format: str = "json"
    max_file_size_mb: int = 100

@dataclass
class SecurityConfig:
    """Security configuration settings."""
    enable_authentication: bool = False
    api_key_required: bool = False

@dataclass
class AppConfig:
    """Main application configuration."""
    server: ServerConfig = field(default_factory=ServerConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    analysis: AnalysisConfig = field(default_factory=AnalysisConfig)
    export: ExportConfig = field(default_factory=ExportConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'AppConfig':
        """
        Create a configuration object from a dictionary.
        
        Args:
            config_dict: Dictionary containing configuration values
            
        Returns:
            AppConfig object with values from the dictionary
        """
        # Start with default config
        result = cls()
        
        # Update with provided values
        if "server" in config_dict:
            result.server = ServerConfig(**config_dict["server"])
        
        if "database" in config_dict:
            result.database = DatabaseConfig(**config_dict["database"])
        
        if "analysis" in config_dict:
            result.analysis = AnalysisConfig(**config_dict["analysis"])
        
        if "export" in config_dict:
            result.export = ExportConfig(**config_dict["export"])
        
        if "security" in config_dict:
            result.security = SecurityConfig(**config_dict["security"])
        
        return result
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the configuration to a dictionary.
        
        Returns:
            Dictionary representation of the configuration
        """
        return {
            "server": asdict(self.server),
            "database": asdict(self.database),
            "analysis": asdict(self.analysis),
            "export": asdict(self.export),
            "security": asdict(self.security)
        }

class ConfigManager:
    """
    Configuration manager to load and access application configuration.
    
    Supports loading configuration from environment variables, JSON files,
    and programmatic settings.
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_file: Optional path to a JSON configuration file
        """
        # Start with default configuration
        self.config = AppConfig.from_dict(DEFAULT_CONFIG)
        
        # Load from file if provided
        if config_file:
            self.load_from_file(config_file)
        
        # Override with environment variables
        self.load_from_env()
        
        # Log the configuration
        logger.debug(f"Initialized configuration: {self.config.to_dict()}")
    
    def load_from_file(self, config_file: str) -> None:
        """
        Load configuration from a JSON file.
        
        Args:
            config_file: Path to a JSON configuration file
        """
        try:
            if not os.path.exists(config_file):
                logger.warning(f"Configuration file not found: {config_file}")
                return
            
            with open(config_file, 'r') as f:
                file_config = json.load(f)
            
            # Update configuration with values from file
            self.update_config(file_config)
            logger.info(f"Loaded configuration from file: {config_file}")
        
        except Exception as e:
            logger.error(f"Failed to load configuration from file {config_file}: {str(e)}")
    
    def load_from_env(self) -> None:
        """
        Load configuration from environment variables.
        
        Looks for variables with the prefix MCP_ and maps them to
        configuration settings.
        """
        try:
            # Server settings
            if "MCP_SERVER_HOST" in os.environ:
                self.config.server.host = os.environ["MCP_SERVER_HOST"]
            
            if "MCP_SERVER_PORT" in os.environ:
                self.config.server.port = int(os.environ["MCP_SERVER_PORT"])
            
            if "MCP_SERVER_DEBUG" in os.environ:
                self.config.server.debug = os.environ["MCP_SERVER_DEBUG"].lower() in ("true", "1", "yes")
            
            if "MCP_LOG_LEVEL" in os.environ:
                self.config.server.log_level = os.environ["MCP_LOG_LEVEL"]
            
            # Database settings
            if "MCP_DB_USE_MOCK" in os.environ:
                self.config.database.use_mock = os.environ["MCP_DB_USE_MOCK"].lower() in ("true", "1", "yes")
            
            if "MCP_DB_TIMEOUT" in os.environ:
                self.config.database.connection_timeout = float(os.environ["MCP_DB_TIMEOUT"])
            
            if "MCP_DB_MAX_RETRIES" in os.environ:
                self.config.database.max_retries = int(os.environ["MCP_DB_MAX_RETRIES"])
            
            # Analysis settings
            if "MCP_ANALYSIS_PRECISION" in os.environ:
                self.config.analysis.default_precision = int(os.environ["MCP_ANALYSIS_PRECISION"])
            
            if "MCP_ANALYSIS_MAX_POINTS" in os.environ:
                self.config.analysis.max_data_points = int(os.environ["MCP_ANALYSIS_MAX_POINTS"])
            
            # Export settings
            if "MCP_EXPORT_DIR" in os.environ:
                self.config.export.output_dir = os.environ["MCP_EXPORT_DIR"]
            
            if "MCP_EXPORT_FORMAT" in os.environ:
                self.config.export.default_format = os.environ["MCP_EXPORT_FORMAT"]
            
            if "MCP_EXPORT_MAX_SIZE" in os.environ:
                self.config.export.max_file_size_mb = int(os.environ["MCP_EXPORT_MAX_SIZE"])
            
            # Security settings
            if "MCP_SECURITY_AUTH" in os.environ:
                self.config.security.enable_authentication = os.environ["MCP_SECURITY_AUTH"].lower() in ("true", "1", "yes")
            
            if "MCP_SECURITY_API_KEY" in os.environ:
                self.config.security.api_key_required = os.environ["MCP_SECURITY_API_KEY"].lower() in ("true", "1", "yes")
            
            logger.info("Loaded configuration from environment variables")
        
        except Exception as e:
            logger.error(f"Failed to load configuration from environment variables: {str(e)}")
    
    def update_config(self, config_update: Dict[str, Any]) -> None:
        """
        Update configuration with values from a dictionary.
        
        Args:
            config_update: Dictionary with configuration values to update
        """
        # Create a new config from the update dictionary
        updated_config = AppConfig.from_dict(config_update)
        
        # Merge with current configuration
        self.config = AppConfig.from_dict({**self.config.to_dict(), **updated_config.to_dict()})
        
        logger.info("Updated configuration")
    
    def save_to_file(self, config_file: str) -> None:
        """
        Save current configuration to a JSON file.
        
        Args:
            config_file: Path to save the configuration file
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(os.path.abspath(config_file)), exist_ok=True)
            
            # Write configuration to file
            with open(config_file, 'w') as f:
                json.dump(self.config.to_dict(), f, indent=2)
            
            logger.info(f"Saved configuration to file: {config_file}")
        
        except Exception as e:
            logger.error(f"Failed to save configuration to file {config_file}: {str(e)}")
    
    def get_config(self) -> AppConfig:
        """
        Get the current configuration.
        
        Returns:
            Current AppConfig object
        """
        return self.config

# Global configuration instance
config_manager = ConfigManager()

def get_config() -> AppConfig:
    """
    Get the global configuration.
    
    Returns:
        Current AppConfig object
    """
    return config_manager.config

def load_config(config_file: str) -> AppConfig:
    """
    Load configuration from a file and update the global configuration.
    
    Args:
        config_file: Path to a JSON configuration file
        
    Returns:
        Updated AppConfig object
    """
    global config_manager
    config_manager = ConfigManager(config_file)
    return config_manager.config

def update_config(config_update: Dict[str, Any]) -> AppConfig:
    """
    Update the global configuration with values from a dictionary.
    
    Args:
        config_update: Dictionary with configuration values to update
        
    Returns:
        Updated AppConfig object
    """
    config_manager.update_config(config_update)
    return config_manager.config

def save_config(config_file: str) -> None:
    """
    Save the global configuration to a file.
    
    Args:
        config_file: Path to save the configuration file
    """
    config_manager.save_to_file(config_file)
