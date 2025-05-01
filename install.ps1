# FastMCP Model Context Protocol Server Installer for Windows
# This script installs the MCP server using uv in a PowerShell environment

Write-Host "FastMCP Model Context Protocol Server Installer" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan

# Check if uv is installed
try {
    $uvVersion = uv --version
    Write-Host "Found uv version: $uvVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: uv is not installed." -ForegroundColor Red
    Write-Host "Please install uv first: https://github.com/astral-sh/uv" -ForegroundColor Yellow
    Write-Host "You can install it with: pip install uv" -ForegroundColor Yellow
    exit 1
}

Write-Host "Creating virtual environment with uv..." -ForegroundColor Cyan
uv venv

Write-Host "Installing dependencies with uv..." -ForegroundColor Cyan
.\.venv\Scripts\python.exe -m uv pip install -r requirements.txt

# Datadog API key configuration
Write-Host "`nDatadog API Key Configuration" -ForegroundColor Cyan
Write-Host "----------------------------" -ForegroundColor Cyan
Write-Host "You can configure Datadog API keys in several ways:`n" -ForegroundColor White

Write-Host "1. Set environment variables before starting the server:" -ForegroundColor Yellow
Write-Host "   $env:DATADOG_API_KEY = 'your_api_key'" -ForegroundColor White
Write-Host "   $env:DATADOG_APP_KEY = 'your_app_key'   # Optional" -ForegroundColor White
Write-Host "   $env:DATADOG_SITE = 'datadoghq.com'     # Optional, default: datadoghq.com`n" -ForegroundColor White

Write-Host "2. Create a .env file in the project directory:" -ForegroundColor Yellow
Write-Host "   DATADOG_API_KEY=your_api_key" -ForegroundColor White
Write-Host "   DATADOG_APP_KEY=your_app_key" -ForegroundColor White
Write-Host "   DATADOG_SITE=datadoghq.com`n" -ForegroundColor White

Write-Host "3. Use the configure_datadog tool at runtime`n" -ForegroundColor Yellow

Write-Host "`nInstallation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To run the server using uvicorn:" -ForegroundColor Yellow
Write-Host "  .\.venv\Scripts\python.exe mcp_server.py" -ForegroundColor White
Write-Host ""
Write-Host "To run the server using FastMCP CLI:" -ForegroundColor Yellow
Write-Host "  .\.venv\Scripts\fastmcp.exe dev mcp_server.py" -ForegroundColor White
Write-Host ""
Write-Host "To install as a Claude Desktop tool:" -ForegroundColor Yellow
Write-Host "  .\.venv\Scripts\fastmcp.exe install mcp_server.py --name `"Model Context Protocol Server`"" -ForegroundColor White
Write-Host ""
Write-Host "To install as a Claude Desktop tool with Datadog API key:" -ForegroundColor Yellow
Write-Host "  .\.venv\Scripts\fastmcp.exe install mcp_server.py --name `"Model Context Protocol Server`" -v DATADOG_API_KEY=your_api_key" -ForegroundColor White
Write-Host ""
Write-Host "Installation completed successfully!" -ForegroundColor Green
