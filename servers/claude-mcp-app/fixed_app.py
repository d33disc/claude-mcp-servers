# fixed_app.py
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Optional, List, Dict, Any, Union
import logging
import traceback
import os
import sys

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('mcp_app')

# Import our configuration module
try:
    from config import get_config, load_config
except ImportError as e:
    logger.error(f"Failed to import configuration module: {e}")
    raise

# Import our export utilities
try:
    from export_utils import export_data, ExportError, get_supported_formats
except ImportError as e:
    logger.error(f"Failed to import export utilities: {e}")
    raise

# Import our mock database
try:
    from fake_database import Database
except ImportError as e:
    logger.error(f"Failed to import Database: {e}")
    raise

# Import MCP components with improved error handling for common issues
try:
    from mcp.server.fastmcp import Context, FastMCP
    import pandas as pd
    import numpy as np
except ImportError as e:
    logger.error(f"Failed to import dependencies: {e}")
    logger.error("Make sure you have installed the MCP package and all requirements.")
    logger.error("Try running: pip install mcp-server-sdk")
    logger.error("If you're using 'uvx' commands, make sure UVX is installed.")
    raise

# Custom exceptions for better error handling
class DatabaseConnectionError(Exception):
    """Raised when database connection fails."""
    pass

class AnalysisError(Exception):
    """Raised when data analysis fails."""
    pass

class ReportGenerationError(Exception):
    """Raised when report generation fails."""
    pass

@dataclass
class AppContext:
    """Application context that holds shared resources."""
    db: Optional[Database] = None

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """
    Manages application lifecycle with robust error handling.
    
    Args:
        server: The FastMCP server instance
        
    Yields:
        AppContext object containing shared resources
    """
    # Initialize context with no database initially
    app_context = AppContext()
    
    # Initialize resources on startup
    logger.info("Starting up database connection...")
    try:
        db = await Database.connect()
        app_context.db = db
        logger.info("Database connection established successfully")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        # We still yield the context even if DB fails, to allow partial functionality
        app_context.db = None
    
    try:
        yield app_context
    finally:
        # Cleanup on shutdown
        logger.info("Shutting down database connection...")
        if app_context.db:
            try:
                await app_context.db.disconnect()
                logger.info("Database disconnected successfully")
            except Exception as e:
                logger.error(f"Error during database disconnection: {e}")

# Create a named server with our improved lifespan manager
mcp = FastMCP("Claude Data Analysis Tool", lifespan=app_lifespan)

# Database query tool with error handling
@mcp.tool()
def query_db(ctx: Context) -> str:
    """
    Executes a query against the database.
    
    Returns:
        Query result as a string
    
    Raises:
        DatabaseConnectionError: If database connection is not available
    """
    app_context = ctx.request_context.lifespan_context
    
    # Check if database is available
    if not app_context.db:
        error_msg = "Database connection is not available"
        logger.error(error_msg)
        raise DatabaseConnectionError(error_msg)
    
    try:
        result = app_context.db.query()
        logger.info("Database query executed successfully")
        return result
    except Exception as e:
        error_msg = f"Database query failed: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        raise DatabaseConnectionError(error_msg) from e

# Data analysis tool with improved error handling
@mcp.tool()
def analyze_data(ctx: Context, data: List[Union[int, float]]) -> Dict[str, Any]:
    """
    Analyze a list of numeric data and return statistical measures.
    
    Args:
        data: List of numeric values to analyze
        
    Returns:
        Dictionary with statistical measures
        
    Raises:
        AnalysisError: If analysis fails or input data is invalid
    """
    # Validate input
    if not data:
        error_msg = "Input data list cannot be empty"
        logger.error(error_msg)
        raise AnalysisError(error_msg)
    
    try:
        # Check if all elements are numeric
        if not all(isinstance(x, (int, float)) for x in data):
            error_msg = "All elements in data must be numeric"
            logger.error(error_msg)
            raise AnalysisError(error_msg)
        
        # Convert to pandas DataFrame for analysis
        df = pd.DataFrame(data)
        
        result = {
            "mean": float(df.mean().iloc[0]),
            "median": float(df.median().iloc[0]),
            "std_dev": float(df.std().iloc[0]),
            "min": float(df.min().iloc[0]),
            "max": float(df.max().iloc[0]),
            "count": len(data)
        }
        
        logger.info(f"Successfully analyzed {len(data)} data points")
        return result
    except Exception as e:
        if isinstance(e, AnalysisError):
            raise
        error_msg = f"Data analysis failed: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        raise AnalysisError(error_msg) from e

# Generate report tool with improved validation and error handling
@mcp.tool()
def generate_report(ctx: Context, title: str, data: Dict[str, Any]) -> str:
    """
    Generate a markdown report from provided data.
    
    Args:
        title: Report title
        data: Dictionary of data to include in the report
        
    Returns:
        Markdown formatted report
        
    Raises:
        ReportGenerationError: If report generation fails or input is invalid
    """
    # Validate inputs
    if not title:
        error_msg = "Report title cannot be empty"
        logger.error(error_msg)
        raise ReportGenerationError(error_msg)
    
    if not data:
        error_msg = "Report data cannot be empty"
        logger.error(error_msg)
        raise ReportGenerationError(error_msg)
    
    try:
        report = f"# {title}\n\n"
        
        for section, content in data.items():
            # Create section heading
            report += f"## {section.title()}\n\n"
            
            # Process content based on type
            if isinstance(content, dict):
                for key, value in content.items():
                    report += f"- **{key}**: {value}\n"
            elif isinstance(content, list):
                for item in content:
                    report += f"- {item}\n"
            else:
                report += f"{content}\n"
            
            # Add spacing between sections
            report += "\n"
        
        logger.info(f"Generated report '{title}' with {len(data)} sections")
        return report
    except Exception as e:
        if isinstance(e, ReportGenerationError):
            raise
        error_msg = f"Report generation failed: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        raise ReportGenerationError(error_msg) from e

# New tool: data validation
@mcp.tool()
def validate_data(ctx: Context, data: List[Any], expected_type: str = "numeric") -> Dict[str, Any]:
    """
    Validates a list of data against expected types.
    
    Args:
        data: List of data to validate
        expected_type: Type to validate against ('numeric', 'string', 'boolean')
        
    Returns:
        Validation results
    """
    if not data:
        return {
            "valid": False,
            "error": "Input data list cannot be empty",
            "valid_count": 0,
            "invalid_count": 0
        }
    
    valid_count = 0
    invalid_values = []
    
    try:
        if expected_type == "numeric":
            check_func = lambda x: isinstance(x, (int, float))
        elif expected_type == "string":
            check_func = lambda x: isinstance(x, str)
        elif expected_type == "boolean":
            check_func = lambda x: isinstance(x, bool)
        else:
            return {
                "valid": False,
                "error": f"Unknown expected_type: {expected_type}",
                "valid_count": 0,
                "invalid_count": len(data)
            }
        
        for i, item in enumerate(data):
            if check_func(item):
                valid_count += 1
            else:
                invalid_values.append({
                    "index": i,
                    "value": str(item),
                    "actual_type": type(item).__name__
                })
        
        return {
            "valid": valid_count == len(data),
            "valid_count": valid_count,
            "invalid_count": len(data) - valid_count,
            "invalid_values": invalid_values[:10] if invalid_values else []  # Limit to first 10 for brevity
        }
    except Exception as e:
        logger.error(f"Data validation failed: {e}")
        return {
            "valid": False,
            "error": str(e),
            "valid_count": valid_count,
            "invalid_count": len(data) - valid_count
        }

# Make the server available as an importable module
if __name__ == "__main__":
    logger.info("MCP server imported successfully")
