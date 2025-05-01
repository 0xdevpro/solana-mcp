"""
Main entry point for the Solana MCP Server
"""
from fastmcp import FastMCP
from app import app
from app.core.config import SERVER_HOST, SERVER_PORT

# Expose app
mcp = app

def main():
    """
    Run the Solana MCP Server with configuration from core/config.py
    """
    print(f"Starting Solana MCP Server at http://{SERVER_HOST}:{SERVER_PORT}")
    print(f"Documentation available at http://{SERVER_HOST}:{SERVER_PORT}/docs")
    print(f"SERVER_PORT: {SERVER_PORT}")
    # Run the server with FastMCP
    app.run(
        host=SERVER_HOST,
        port=SERVER_PORT,
        transport="sse"
    )

if __name__ == "__main__":
    main()
