#!/bin/bash

# FastMCP MCP Server installer script
# This script installs the MCP server using uv

set -e

echo "FastMCP Model Context Protocol Server Installer"
echo "==============================================="

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Error: uv is not installed."
    echo "Please install uv first: https://github.com/astral-sh/uv"
    echo "You can install it with: pip install uv"
    exit 1
fi

echo "Creating virtual environment with uv..."
uv venv

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing dependencies with uv..."
uv pip install -r requirements.txt

# Datadog API key configuration
echo ""
echo "Datadog API Key Configuration"
echo "----------------------------"
echo "You can configure Datadog API keys in several ways:"
echo ""
echo "1. Set environment variables before starting the server:"
echo "   export DATADOG_API_KEY=your_api_key"
echo "   export DATADOG_APP_KEY=your_app_key   # Optional"
echo "   export DATADOG_SITE=datadoghq.com     # Optional, default: datadoghq.com"
echo ""
echo "2. Create a .env file in the project directory:"
echo "   DATADOG_API_KEY=your_api_key"
echo "   DATADOG_APP_KEY=your_app_key"
echo "   DATADOG_SITE=datadoghq.com"
echo ""
echo "3. Use the configure_datadog tool at runtime"
echo ""

echo "Installation complete!"
echo ""
echo "To run the server using uvicorn:"
echo "  source .venv/bin/activate"
echo "  python mcp_server.py"
echo ""
echo "To run the server using FastMCP CLI:"
echo "  source .venv/bin/activate"
echo "  fastmcp dev mcp_server.py"
echo ""
echo "To install as a Claude Desktop tool:"
echo "  source .venv/bin/activate"
echo "  fastmcp install mcp_server.py --name \"Model Context Protocol Server\""
echo ""
echo "To install as a Claude Desktop tool with Datadog API key:"
echo "  source .venv/bin/activate"
echo "  fastmcp install mcp_server.py --name \"Model Context Protocol Server\" -v DATADOG_API_KEY=your_api_key"
echo ""
echo "Installation completed successfully!"
