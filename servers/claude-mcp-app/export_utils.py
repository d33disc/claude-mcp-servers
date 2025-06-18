# export_utils.py
"""
Utility functions for exporting analysis results to various formats.

This module provides functions to export data in CSV, JSON, and other formats,
making it easy to save and share analysis results from the MCP server.
"""

import csv
import json
import logging
import os
import yaml
import xlsxwriter
import pickle
import sqlite3
import pandas as pd
from typing import Any, Dict, List, Optional, Union, Tuple
import xml.dom.minidom
import xml.etree.ElementTree as ET
from config import get_config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('export_utils')

class ExportError(Exception):
    """Raised when export operations fail."""
    pass

def export_to_csv(data: List[Dict[str, Any]], filename: str, headers: Optional[List[str]] = None) -> str:
    """
    Export data to a CSV file.
    
    Args:
        data: List of dictionaries to export
        filename: Output filename (will append .csv if not present)
        headers: Optional list of column headers (uses dictionary keys if not provided)
        
    Returns:
        Path to the exported file
        
    Raises:
        ExportError: If the export operation fails
    """
    try:
        # Ensure filename has .csv extension
        if not filename.lower().endswith('.csv'):
            filename += '.csv'
        
        # If headers are not provided, use keys from the first data item
        if headers is None and data:
            headers = list(data[0].keys())
        
        # Write data to CSV file
        with open(filename, 'w', newline='') as csvfile:
            if headers:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data)
            else:
                # Handle empty data case
                csvfile.write('')
        
        logger.info(f"Exported {len(data)} records to CSV file: {filename}")
        return os.path.abspath(filename)
    
    except Exception as e:
        error_msg = f"Failed to export data to CSV: {str(e)}"
        logger.error(error_msg)
        raise ExportError(error_msg) from e

def export_to_json(data: Any, filename: str, pretty: bool = True) -> str:
    """
    Export data to a JSON file.
    
    Args:
        data: Data to export (can be dict, list, or other JSON-serializable object)
        filename: Output filename (will append .json if not present)
        pretty: Whether to format JSON with indentation for readability
        
    Returns:
        Path to the exported file
        
    Raises:
        ExportError: If the export operation fails
    """
    try:
        # Ensure filename has .json extension
        if not filename.lower().endswith('.json'):
            filename += '.json'
        
        # Write data to JSON file
        with open(filename, 'w') as jsonfile:
            if pretty:
                json.dump(data, jsonfile, indent=2)
            else:
                json.dump(data, jsonfile)
        
        logger.info(f"Exported data to JSON file: {filename}")
        return os.path.abspath(filename)
    
    except Exception as e:
        error_msg = f"Failed to export data to JSON: {str(e)}"
        logger.error(error_msg)
        raise ExportError(error_msg) from e

def export_to_xml(data: Dict[str, Any], filename: str, root_element: str = "data") -> str:
    """
    Export data to an XML file.
    
    Args:
        data: Dictionary to export
        filename: Output filename (will append .xml if not present)
        root_element: Name for the root XML element
        
    Returns:
        Path to the exported file
        
    Raises:
        ExportError: If the export operation fails
    """
    try:
        # Ensure filename has .xml extension
        if not filename.lower().endswith('.xml'):
            filename += '.xml'
        
        # Create root element
        root = ET.Element(root_element)
        
        # Helper function to convert dict to XML recursively
        def dict_to_xml(parent: ET.Element, data: Dict[str, Any]) -> None:
            for key, value in data.items():
                # Convert key to valid XML element name (remove spaces, special chars)
                element_name = ''.join(c for c in str(key) if c.isalnum() or c == '_')
                if not element_name:
                    element_name = "item"
                
                # Handle different value types
                if isinstance(value, dict):
                    subelem = ET.SubElement(parent, element_name)
                    dict_to_xml(subelem, value)
                elif isinstance(value, list):
                    subelem = ET.SubElement(parent, element_name)
                    for item in value:
                        if isinstance(item, dict):
                            item_elem = ET.SubElement(subelem, "item")
                            dict_to_xml(item_elem, item)
                        else:
                            item_elem = ET.SubElement(subelem, "item")
                            item_elem.text = str(item)
                else:
                    subelem = ET.SubElement(parent, element_name)
                    subelem.text = str(value)
        
        # Convert data to XML
        dict_to_xml(root, data)
        
        # Create pretty XML string
        xml_string = xml.dom.minidom.parseString(
            ET.tostring(root, encoding='unicode')
        ).toprettyxml(indent="  ")
        
        # Write to file
        with open(filename, 'w') as xmlfile:
            xmlfile.write(xml_string)
        
        logger.info(f"Exported data to XML file: {filename}")
        return os.path.abspath(filename)
    
    except Exception as e:
        error_msg = f"Failed to export data to XML: {str(e)}"
        logger.error(error_msg)
        raise ExportError(error_msg) from e

def export_to_markdown(data: Dict[str, Any], filename: str, title: str = "Exported Data") -> str:
    """
    Export data to a Markdown file.
    
    Args:
        data: Dictionary to export
        filename: Output filename (will append .md if not present)
        title: Title for the markdown document
        
    Returns:
        Path to the exported file
        
    Raises:
        ExportError: If the export operation fails
    """
    try:
        # Ensure filename has .md extension
        if not filename.lower().endswith('.md'):
            filename += '.md'
        
        # Start with the title
        markdown = f"# {title}\n\n"
        
        # Helper function to convert dict to markdown recursively
        def dict_to_markdown(data: Dict[str, Any], level: int = 1) -> str:
            md = ""
            for key, value in data.items():
                # Create header for each section
                md += f"{'#' * (level + 1)} {key}\n\n"
                
                # Handle different value types
                if isinstance(value, dict):
                    md += dict_to_markdown(value, level + 1)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            md += dict_to_markdown(item, level + 1)
                        else:
                            md += f"- {item}\n"
                    md += "\n"
                else:
                    md += f"{value}\n\n"
            
            return md
        
        # Convert data to markdown
        markdown += dict_to_markdown(data)
        
        # Write to file
        with open(filename, 'w') as mdfile:
            mdfile.write(markdown)
        
        logger.info(f"Exported data to Markdown file: {filename}")
        return os.path.abspath(filename)
    
    except Exception as e:
        error_msg = f"Failed to export data to Markdown: {str(e)}"
        logger.error(error_msg)
        raise ExportError(error_msg) from e

def export_to_html(data: Dict[str, Any], filename: str, title: str = "Exported Data") -> str:
    """
    Export data to an HTML file.
    
    Args:
        data: Dictionary to export
        filename: Output filename (will append .html if not present)
        title: Title for the HTML document
        
    Returns:
        Path to the exported file
        
    Raises:
        ExportError: If the export operation fails
    """
    try:
        # Ensure filename has .html extension
        if not filename.lower().endswith('.html'):
            filename += '.html'
        
        # Create HTML header with title and basic styling
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; color: #333; }}
        h1 {{ color: #2c3e50; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
        h2, h3, h4 {{ color: #2c3e50; margin-top: 20px; }}
        table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
        th, td {{ text-align: left; padding: 12px; }}
        th {{ background-color: #f2f2f2; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
"""
        
        # Helper function to convert dict to HTML recursively
        def dict_to_html(data: Dict[str, Any], level: int = 1) -> str:
            html_content = ""
            for key, value in data.items():
                # Create header for each section
                html_content += f"<h{level + 1}>{key}</h{level + 1}>\n"
                
                # Handle different value types
                if isinstance(value, dict):
                    html_content += dict_to_html(value, level + 1)
                elif isinstance(value, list):
                    if all(isinstance(item, dict) for item in value):
                        # Create a table for list of dictionaries
                        if value:
                            headers = value[0].keys()
                            html_content += "<table>\n<tr>\n"
                            for header in headers:
                                html_content += f"<th>{header}</th>\n"
                            html_content += "</tr>\n"
                            
                            for item in value:
                                html_content += "<tr>\n"
                                for header in headers:
                                    cell_value = item.get(header, "")
                                    html_content += f"<td>{cell_value}</td>\n"
                                html_content += "</tr>\n"
                            
                            html_content += "</table>\n"
                    else:
                        # Create a list for simple items
                        html_content += "<ul>\n"
                        for item in value:
                            html_content += f"<li>{item}</li>\n"
                        html_content += "</ul>\n"
                else:
                    html_content += f"<p>{value}</p>\n"
            
            return html_content
        
        # Convert data to HTML
        html += dict_to_html(data)
        
        # Close HTML tags
        html += """    </div>
</body>
</html>
"""
        
        # Write to file
        with open(filename, 'w') as htmlfile:
            htmlfile.write(html)
        
        logger.info(f"Exported data to HTML file: {filename}")
        return os.path.abspath(filename)
    
    except Exception as e:
        error_msg = f"Failed to export data to HTML: {str(e)}"
        logger.error(error_msg)
        raise ExportError(error_msg) from e

def export_to_yaml(data: Any, filename: str) -> str:
    """
    Export data to a YAML file.
    
    Args:
        data: Data to export (can be dict, list, or other YAML-serializable object)
        filename: Output filename (will append .yaml if not present)
        
    Returns:
        Path to the exported file
        
    Raises:
        ExportError: If the export operation fails
    """
    try:
        # Ensure filename has .yaml extension
        if not filename.lower().endswith(('.yaml', '.yml')):
            filename += '.yaml'
        
        # Write data to YAML file
        with open(filename, 'w') as yamlfile:
            yaml.dump(data, yamlfile, default_flow_style=False, sort_keys=False)
        
        logger.info(f"Exported data to YAML file: {filename}")
        return os.path.abspath(filename)
    
    except Exception as e:
        error_msg = f"Failed to export data to YAML: {str(e)}"
        logger.error(error_msg)
        raise ExportError(error_msg) from e

def export_to_excel(data: List[Dict[str, Any]], filename: str, sheet_name: str = "Data") -> str:
    """
    Export data to an Excel file.
    
    Args:
        data: List of dictionaries to export
        filename: Output filename (will append .xlsx if not present)
        sheet_name: Name for the worksheet
        
    Returns:
        Path to the exported file
        
    Raises:
        ExportError: If the export operation fails
    """
    try:
        # Ensure filename has .xlsx extension
        if not filename.lower().endswith('.xlsx'):
            filename += '.xlsx'
        
        # Convert data to DataFrame for easier Excel export
        df = pd.DataFrame(data)
        
        # Create Excel writer
        writer = pd.ExcelWriter(filename, engine='xlsxwriter')
        
        # Write DataFrame to Excel
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        # Get workbook and worksheet objects
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]
        
        # Add formatting
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#D9E1F2',
            'border': 1
        })
        
        # Format header row
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
        
        # Auto-adjust column widths
        for col_num, column in enumerate(df.columns):
            max_width = max(
                df[column].astype(str).map(len).max(),
                len(str(column))
            )
            worksheet.set_column(col_num, col_num, max_width + 2)
        
        # Close the writer
        writer.close()
        
        logger.info(f"Exported {len(data)} records to Excel file: {filename}")
        return os.path.abspath(filename)
    
    except Exception as e:
        error_msg = f"Failed to export data to Excel: {str(e)}"
        logger.error(error_msg)
        raise ExportError(error_msg) from e

def export_to_sqlite(data: List[Dict[str, Any]], filename: str, table_name: str = "data") -> str:
    """
    Export data to a SQLite database file.
    
    Args:
        data: List of dictionaries to export
        filename: Output filename (will append .db if not present)
        table_name: Name for the database table
        
    Returns:
        Path to the exported file
        
    Raises:
        ExportError: If the export operation fails
    """
    try:
        # Ensure filename has .db extension
        if not filename.lower().endswith('.db'):
            filename += '.db'
        
        # Convert data to DataFrame
        df = pd.DataFrame(data)
        
        # Create SQLite connection
        conn = sqlite3.connect(filename)
        
        # Write data to SQLite database
        df.to_sql(table_name, conn, index=False, if_exists='replace')
        
        # Close connection
        conn.close()
        
        logger.info(f"Exported {len(data)} records to SQLite database: {filename}")
        return os.path.abspath(filename)
    
    except Exception as e:
        error_msg = f"Failed to export data to SQLite: {str(e)}"
        logger.error(error_msg)
        raise ExportError(error_msg) from e

def export_to_pickle(data: Any, filename: str) -> str:
    """
    Export data to a Python pickle file (for serialization).
    
    Args:
        data: Data to export (can be any Python object)
        filename: Output filename (will append .pkl if not present)
        
    Returns:
        Path to the exported file
        
    Raises:
        ExportError: If the export operation fails
    """
    try:
        # Ensure filename has .pkl extension
        if not filename.lower().endswith(('.pkl', '.pickle')):
            filename += '.pkl'
        
        # Write data to pickle file
        with open(filename, 'wb') as picklefile:
            pickle.dump(data, picklefile)
        
        logger.info(f"Exported data to pickle file: {filename}")
        return os.path.abspath(filename)
    
    except Exception as e:
        error_msg = f"Failed to export data to pickle: {str(e)}"
        logger.error(error_msg)
        raise ExportError(error_msg) from e

def get_supported_formats() -> List[str]:
    """
    Get a list of supported export formats.
    
    Returns:
        List of supported format names
    """
    return ["csv", "json", "xml", "markdown", "html", "yaml", "excel", "sqlite", "pickle"]

def export_data(data: Any, filename: str, format: str = None) -> str:
    """
    Export data to a file in the specified format.
    
    Args:
        data: Data to export
        filename: Output filename
        format: Format to use (csv, json, xml, markdown, html, yaml, excel, sqlite, pickle)
               If None, infer from filename extension or use configured default
        
    Returns:
        Path to the exported file
        
    Raises:
        ExportError: If the export operation fails or format is unsupported
    """
    # If format not specified, try to infer from filename or use default
    if format is None:
        # Check for file extension
        _, ext = os.path.splitext(filename)
        if ext:
            format = ext.lower().lstrip('.')
        else:
            # Use default format from config
            config = get_config()
            format = config.export.default_format
    
    # Ensure the output directory exists
    config = get_config()
    output_dir = config.export.output_dir
    if output_dir and not os.path.isabs(filename):
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.join(output_dir, filename)
    
    # Export based on format
    try:
        if format in ['csv']:
            # For CSV, data should be a list of dictionaries
            if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
                raise ExportError("CSV export requires a list of dictionaries")
            return export_to_csv(data, filename)
        
        elif format in ['json']:
            return export_to_json(data, filename)
        
        elif format in ['xml']:
            # For XML, data should be a dictionary
            if not isinstance(data, dict):
                raise ExportError("XML export requires a dictionary")
            return export_to_xml(data, filename)
        
        elif format in ['md', 'markdown']:
            # For Markdown, data should be a dictionary
            if not isinstance(data, dict):
                raise ExportError("Markdown export requires a dictionary")
            return export_to_markdown(data, filename)
        
        elif format in ['html']:
            # For HTML, data should be a dictionary
            if not isinstance(data, dict):
                raise ExportError("HTML export requires a dictionary")
            return export_to_html(data, filename)
        
        elif format in ['yaml', 'yml']:
            return export_to_yaml(data, filename)
        
        elif format in ['xlsx', 'excel']:
            # For Excel, data should be a list of dictionaries
            if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
                raise ExportError("Excel export requires a list of dictionaries")
            return export_to_excel(data, filename)
        
        elif format in ['db', 'sqlite']:
            # For SQLite, data should be a list of dictionaries
            if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
                raise ExportError("SQLite export requires a list of dictionaries")
            return export_to_sqlite(data, filename)
        
        elif format in ['pkl', 'pickle']:
            return export_to_pickle(data, filename)
        
        else:
            raise ExportError(f"Unsupported export format: {format}")
    
    except ExportError as e:
        # Re-raise export errors
        raise
    except Exception as e:
        error_msg = f"Failed to export data to {format}: {str(e)}"
        logger.error(error_msg)
        raise ExportError(error_msg) from e
