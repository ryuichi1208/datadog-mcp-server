#!/usr/bin/env python3
"""
FastMCP Server - Model Context Protocol implementation using FastMCP library
A lightweight server for managing model contexts
"""

from fastmcp import FastMCP
from fastmcp.types import File
from typing import Dict, Any, List, Optional
import os
import logging

# Logger configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("fastmcp-server")

# Read Datadog API key from environment variable
DATADOG_API_KEY = os.environ.get("DATADOG_API_KEY")
DATADOG_APP_KEY = os.environ.get("DATADOG_APP_KEY")
DATADOG_SITE = os.environ.get("DATADOG_SITE", "datadoghq.com")

# Create FastMCP instance
mcp = FastMCP("Model Context Protocol Server")

# In-memory storage (for a real-world application, consider using a database)
contexts = {}

# Datadog integration
datadog_initialized = False


def initialize_datadog():
    """Initialize Datadog integration if API key is provided"""
    global datadog_initialized

    if DATADOG_API_KEY:
        try:
            from datadog import initialize, api

            options = {
                "api_key": DATADOG_API_KEY,
                "app_key": DATADOG_APP_KEY,
                "api_host": f"https://api.{DATADOG_SITE}",
            }

            initialize(**options)
            datadog_initialized = True
            logger.info("Datadog integration initialized successfully")
            return True
        except ImportError:
            logger.warning("Datadog package not installed, metrics will not be reported")
        except Exception as e:
            logger.error(f"Failed to initialize Datadog: {str(e)}")
    else:
        logger.info("No Datadog API key provided, metrics will not be reported")

    return False


def send_metric(name: str, value: float, tags: Optional[List[str]] = None):
    """Send a metric to Datadog if integration is enabled"""
    if not datadog_initialized:
        return

    try:
        from datadog import api

        api.Metric.send(metric=name, points=value, tags=tags or [])
        logger.debug(f"Sent metric {name}={value} to Datadog")
    except Exception as e:
        logger.error(f"Failed to send metric to Datadog: {str(e)}")


@mcp.tool()
def configure_datadog(api_key: str, app_key: Optional[str] = None, site: Optional[str] = None) -> Dict[str, Any]:
    """
    Configure Datadog integration with the provided credentials

    Args:
        api_key: Datadog API key
        app_key: Optional Datadog application key
        site: Optional Datadog site (default: datadoghq.com)

    Returns:
        Status information
    """
    global DATADOG_API_KEY, DATADOG_APP_KEY, DATADOG_SITE

    DATADOG_API_KEY = api_key
    if app_key:
        DATADOG_APP_KEY = app_key
    if site:
        DATADOG_SITE = site

    success = initialize_datadog()

    return {
        "status": "configured" if success else "failed",
        "datadog_integration": "enabled" if success else "disabled",
        "site": DATADOG_SITE,
    }


@mcp.tool()
def create_context(
    context_id: str, model_name: str, data: Dict[str, Any], tags: Optional[List[str]] = None
) -> Dict[str, str]:
    """
    Create a new model context with the specified parameters

    Args:
        context_id: Unique identifier for the context
        model_name: Name of the model associated with this context
        data: Context data dictionary
        tags: Optional list of tags for categorization

    Returns:
        Status information including the context ID
    """
    if context_id in contexts:
        return {"status": "error", "message": "Context ID already exists"}

    context = {"context_id": context_id, "model_name": model_name, "data": data, "tags": tags or []}

    contexts[context_id] = context
    logger.info(f"Created context: {context_id}")

    # Send metric to Datadog if integration is enabled
    if datadog_initialized:
        send_metric("mcp.contexts.created", 1, tags=["model:" + model_name])
        send_metric("mcp.contexts.total", len(contexts))

    return {"status": "created", "context_id": context_id}


@mcp.tool()
def get_context(context_id: str) -> Dict[str, Any]:
    """
    Retrieve a specific context by its ID

    Args:
        context_id: ID of the context to retrieve

    Returns:
        The complete context object
    """
    if context_id not in contexts:
        return {"status": "error", "message": "Context ID not found"}

    # Send metric to Datadog if integration is enabled
    if datadog_initialized:
        model_name = contexts[context_id]["model_name"]
        send_metric("mcp.contexts.accessed", 1, tags=["model:" + model_name])

    return contexts[context_id]


@mcp.tool()
def update_context(
    context_id: str, model_name: str, data: Dict[str, Any], tags: Optional[List[str]] = None
) -> Dict[str, str]:
    """
    Update an existing context with new values

    Args:
        context_id: ID of the context to update
        model_name: New model name
        data: New context data
        tags: New list of tags

    Returns:
        Status information including the context ID
    """
    if context_id not in contexts:
        return {"status": "error", "message": "Context ID not found"}

    old_model_name = contexts[context_id]["model_name"]

    context = {"context_id": context_id, "model_name": model_name, "data": data, "tags": tags or []}

    contexts[context_id] = context
    logger.info(f"Updated context: {context_id}")

    # Send metric to Datadog if integration is enabled
    if datadog_initialized:
        send_metric("mcp.contexts.updated", 1, tags=["old_model:" + old_model_name, "new_model:" + model_name])

    return {"status": "updated", "context_id": context_id}


@mcp.tool()
def delete_context(context_id: str) -> Dict[str, str]:
    """
    Delete a context by its ID

    Args:
        context_id: ID of the context to delete

    Returns:
        Status information
    """
    if context_id not in contexts:
        return {"status": "error", "message": "Context ID not found"}

    model_name = contexts[context_id]["model_name"]
    del contexts[context_id]
    logger.info(f"Deleted context: {context_id}")

    # Send metric to Datadog if integration is enabled
    if datadog_initialized:
        send_metric("mcp.contexts.deleted", 1, tags=["model:" + model_name])
        send_metric("mcp.contexts.total", len(contexts))

    return {"status": "deleted", "context_id": context_id}


@mcp.tool()
def list_contexts(model_name: Optional[str] = None, tag: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    List all contexts with optional filtering by model name or tag

    Args:
        model_name: Filter contexts by model name
        tag: Filter contexts by tag

    Returns:
        List of context objects matching the filters
    """
    results = list(contexts.values())

    if model_name:
        results = [item for item in results if item["model_name"] == model_name]

    if tag:
        results = [item for item in results if tag in item["tags"]]

    # Send metric to Datadog if integration is enabled
    if datadog_initialized:
        tags = []
        if model_name:
            tags.append("filtered_by_model:" + model_name)
        if tag:
            tags.append("filtered_by_tag:" + tag)
        send_metric("mcp.contexts.listed", 1, tags=tags)

    return results


@mcp.tool()
def query_model(context_id: str, query_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a query against a specific context

    Args:
        context_id: ID of the context to query
        query_data: Query parameters

    Returns:
        Query results
    """
    if context_id not in contexts:
        return {"status": "error", "message": "Context ID not found"}

    context = contexts[context_id]
    logger.info(f"Executing query on context: {context_id}")

    # Process the query (simplified example)
    result = {
        "context_id": context_id,
        "model_name": context["model_name"],
        "query": query_data,
        "result": {"processed": True, "timestamp": "2023-11-01T12:00:00Z"},
    }

    # Send metric to Datadog if integration is enabled
    if datadog_initialized:
        send_metric("mcp.queries.executed", 1, tags=["model:" + context["model_name"]])

    return result


@mcp.tool()
def health_check() -> Dict[str, Any]:
    """
    Check the health status of the server

    Returns:
        Health status information
    """
    return {
        "status": "healthy",
        "contexts_count": len(contexts),
        "version": "1.0.0",
        "datadog_integration": "enabled" if datadog_initialized else "disabled",
    }


@mcp.on_startup()
async def startup():
    """Initialize server resources on startup"""
    logger.info("Starting FastMCP server")
    initialize_datadog()

    # Send startup metric to Datadog if integration is enabled
    if datadog_initialized:
        send_metric("mcp.server.startup", 1)


@mcp.on_shutdown()
async def shutdown():
    """Clean up resources on shutdown"""
    logger.info("Shutting down FastMCP server")

    # Send shutdown metric to Datadog if integration is enabled
    if datadog_initialized:
        send_metric("mcp.server.shutdown", 1)


# Define a prompt template that explains how to use this MCP server
mcp.define_prompt(
    """
# Model Context Protocol Server

This MCP server provides tools for managing model contexts. You can:

- Create new contexts with `create_context`
- Retrieve contexts with `get_context`
- Update existing contexts with `update_context`
- Delete contexts with `delete_context`
- List and filter contexts with `list_contexts`
- Execute queries against contexts with `query_model`
- Check server health with `health_check`

## Datadog Integration

To configure Datadog integration:

1. Provide API key via environment variable (DATADOG_API_KEY)
2. Optionally set APP_KEY (DATADOG_APP_KEY) and site (DATADOG_SITE)
3. Or use the `configure_datadog` tool to set credentials at runtime

Each context has an ID, model name, data dictionary, and optional tags.
"""
)

if __name__ == "__main__":
    # Run the server
    mcp.run()
