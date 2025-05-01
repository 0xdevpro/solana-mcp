"""
API endpoints for Solana MCP Server
"""
from fastmcp import FastMCP

# Create the FastMCP application
app = FastMCP("Solana MCP")

# Register endpoints
from app.api import info
from app.api import solana
