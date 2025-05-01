#!/usr/bin/env python3
"""
Example client script that demonstrates how to use the Model Context Protocol server
"""

import asyncio
from fastmcp import Client


async def main():
    """Run example operations with the MCP server"""
    # Connect to the MCP server
    async with Client() as client:
        print("Connected to MCP server")

        # Check server health
        health = await client.call_tool("health_check")
        print(f"Server health: {health}")

        # Create a new context
        context_id = "example-context"
        create_result = await client.call_tool(
            "create_context",
            {
                "context_id": context_id,
                "model_name": "gpt-4",
                "data": {"parameters": {"temperature": 0.7, "max_tokens": 500}},
                "tags": ["example", "demo"],
            },
        )
        print(f"Context creation result: {create_result}")

        # Get the context
        context = await client.call_tool("get_context", {"context_id": context_id})
        print(f"Retrieved context: {context}")

        # List all contexts
        contexts = await client.call_tool("list_contexts")
        print(f"All contexts: {contexts}")

        # Filter contexts by tag
        tagged_contexts = await client.call_tool("list_contexts", {"tag": "example"})
        print(f"Contexts with 'example' tag: {tagged_contexts}")

        # Execute a query
        query_result = await client.call_tool(
            "query_model",
            {"context_id": context_id, "query_data": {"prompt": "Hello, world!", "options": {"stream": False}}},
        )
        print(f"Query result: {query_result}")

        # Update the context
        update_result = await client.call_tool(
            "update_context",
            {
                "context_id": context_id,
                "model_name": "gpt-4",
                "data": {"parameters": {"temperature": 0.5, "max_tokens": 500}},  # Changed from 0.7
                "tags": ["example", "demo", "updated"],  # Added "updated" tag
            },
        )
        print(f"Context update result: {update_result}")

        # Delete the context
        delete_result = await client.call_tool("delete_context", {"context_id": context_id})
        print(f"Context deletion result: {delete_result}")

        # Verify deletion
        contexts_after = await client.call_tool("list_contexts")
        print(f"Contexts after deletion: {contexts_after}")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
