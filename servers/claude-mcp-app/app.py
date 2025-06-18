# app.py
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
from fake_database import Database  # Our mock database
from mcp.server.fastmcp import Context, FastMCP
import pandas as pd
import numpy as np

# Create a named server
mcp = FastMCP("Claude Data Analysis Tool")

@dataclass
class AppContext:
    db: Database

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with type-safe context"""
    # Initialize on startup
    print("Starting up database connection...")
    db = await Database.connect()
    try:
        yield AppContext(db=db)
    finally:
        # Cleanup on shutdown
        print("Shutting down database connection...")
        await db.disconnect()

# Pass lifespan to server
mcp = FastMCP("Claude Data Analysis Tool", lifespan=app_lifespan)

# Database query tool
@mcp.tool()
def query_db(ctx: Context) -> str:
    """Tool that uses initialized database resource"""
    app_context = ctx.request_context.lifespan_context
    db = app_context.db
    return db.query()

# Data analysis tool
@mcp.tool()
def analyze_data(ctx: Context, data: list) -> dict:
    """
    Analyze a list of data and return statistics
    
    Args:
        data: List of numeric values to analyze
        
    Returns:
        Dictionary with statistical measures
    """
    df = pd.DataFrame(data)
    
    return {
        "mean": float(df.mean().iloc[0]),
        "median": float(df.median().iloc[0]),
        "std_dev": float(df.std().iloc[0]),
        "min": float(df.min().iloc[0]),
        "max": float(df.max().iloc[0]),
        "count": len(data)
    }

# Generate report tool
@mcp.tool()
def generate_report(ctx: Context, title: str, data: dict) -> str:
    """
    Generate a markdown report from provided data
    
    Args:
        title: Report title
        data: Dictionary of data to include in the report
        
    Returns:
        Markdown formatted report
    """
    report = f"# {title}\n\n"
    
    for section, content in data.items():
        report += f"## {section.title()}\n\n"
        
        if isinstance(content, dict):
            for key, value in content.items():
                report += f"- **{key}**: {value}\n"
        elif isinstance(content, list):
            for item in content:
                report += f"- {item}\n"
        else:
            report += f"{content}\n"
        
        report += "\n"
    
    return report

# Make the server available as an importable module
if __name__ == "__main__":
    print("MCP server imported successfully")
