# FastMCP - Model Context Protocol Server

A lightweight Model Context Protocol (MCP) server implemented with [FastMCP](https://github.com/jlowin/fastmcp), a fast and Pythonic framework for building MCP servers and clients.

## Features

- Create, retrieve, update, and delete model contexts
- Query execution against specific contexts
- Filtering by model name and tags
- In-memory storage (for development)
- FastMCP integration for easy MCP server development
- Datadog integration for metrics and monitoring

## Requirements

- Python 3.7+
- FastMCP
- uv (recommended for environment management)
- Datadog account (optional, for metrics)

## Installation

### Using uv (Recommended)

The simplest way to install is using the provided scripts:

#### Unix/Linux/macOS

```bash
# Clone the repository
git clone https://github.com/yourusername/datadog-mcp-server.git
cd datadog-mcp-server

# Make the install script executable
chmod +x install.sh

# Run the installer
./install.sh
```

#### Windows

```powershell
# Clone the repository
git clone https://github.com/yourusername/datadog-mcp-server.git
cd datadog-mcp-server

# Run the installer
.\install.ps1
```

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/datadog-mcp-server.git
cd datadog-mcp-server

# Create and activate a virtual environment with uv
uv venv
# On Unix/Linux/macOS:
source .venv/bin/activate
# On Windows:
.\.venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt
```

## Datadog Configuration

The server integrates with Datadog for metrics and monitoring. You can configure Datadog API credentials in several ways:

### 1. Environment Variables

Set these environment variables before starting the server:

```bash
# Unix/Linux/macOS
export DATADOG_API_KEY=your_api_key
export DATADOG_APP_KEY=your_app_key  # Optional
export DATADOG_SITE=datadoghq.com    # Optional, default: datadoghq.com

# Windows PowerShell
$env:DATADOG_API_KEY = 'your_api_key'
$env:DATADOG_APP_KEY = 'your_app_key'  # Optional
$env:DATADOG_SITE = 'datadoghq.com'    # Optional
```

### 2. .env File

Create a `.env` file in the project directory:

```
DATADOG_API_KEY=your_api_key
DATADOG_APP_KEY=your_app_key
DATADOG_SITE=datadoghq.com
```

### 3. FastMCP CLI Installation

When installing as a Claude Desktop tool, you can pass environment variables:

```bash
fastmcp install mcp_server.py --name "Model Context Server" -v DATADOG_API_KEY=your_api_key
```

### 4. Runtime Configuration

Use the `configure_datadog` tool at runtime:

```python
result = await client.call_tool("configure_datadog", {
    "api_key": "your_api_key",
    "app_key": "your_app_key",  # Optional
    "site": "datadoghq.com"     # Optional
})
```

## Usage

### Starting the Server

```bash
# Start directly from activated environment
python mcp_server.py

# Or use uv run (no activation needed)
uv run python mcp_server.py

# Use FastMCP CLI for development (if in activated environment)
fastmcp dev mcp_server.py

# Use FastMCP CLI with uv (no activation needed)
uv run -m fastmcp dev mcp_server.py
```

### Installing as a Claude Desktop Tool

```bash
# From activated environment
fastmcp install mcp_server.py --name "Model Context Server"

# Using uv directly
uv run python -m fastmcp install mcp_server.py --name "Model Context Server"

# With Datadog API key
fastmcp install mcp_server.py --name "Model Context Server" -v DATADOG_API_KEY=your_api_key
```

### Using the Tools

The server provides the following tools:

- `create_context` - Create a new context
- `get_context` - Retrieve a specific context
- `update_context` - Update an existing context
- `delete_context` - Delete a context
- `list_contexts` - List all contexts (with optional filtering)
- `query_model` - Execute a query against a specific context
- `health_check` - Server health check
- `configure_datadog` - Configure Datadog integration at runtime

## Example Requests

### Creating a Context

```python
result = await client.call_tool("create_context", {
    "context_id": "model-123",
    "model_name": "gpt-3.5",
    "data": {
        "parameters": {
            "temperature": 0.7
        }
    },
    "tags": ["production", "nlp"]
})
```

### Executing a Query

```python
result = await client.call_tool("query_model", {
    "context_id": "model-123",
    "query_data": {
        "prompt": "Hello, world!"
    }
})
```

### Configuring Datadog

```python
result = await client.call_tool("configure_datadog", {
    "api_key": "your_datadog_api_key",
    "app_key": "your_datadog_app_key",  # Optional
    "site": "datadoghq.com"             # Optional
})
```

## Datadog Metrics

The server reports the following metrics to Datadog:

- `mcp.contexts.created` - Context creation events
- `mcp.contexts.updated` - Context update events
- `mcp.contexts.deleted` - Context deletion events
- `mcp.contexts.accessed` - Context access events
- `mcp.contexts.total` - Total number of contexts
- `mcp.contexts.listed` - List contexts operation events
- `mcp.queries.executed` - Query execution events
- `mcp.server.startup` - Server startup events
- `mcp.server.shutdown` - Server shutdown events

## Development

See the included `mcp_example.py` for a client implementation example:

```bash
# Run the example client (with activated environment)
python mcp_example.py

# Run with uv (no activation needed)
uv run python mcp_example.py
```

## License

MIT

## Resources

- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Model Context Protocol](https://github.com/anthropics/model-context-protocol) specification
- [uv Package Manager](https://github.com/astral-sh/uv)
- [Datadog API Documentation](https://docs.datadoghq.com/api/)
