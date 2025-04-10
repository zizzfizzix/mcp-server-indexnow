import os  # Add os import

from mcp.server.fastmcp import FastMCP

from mcp_server_indexnow.services.indexnow import IndexNowApiClient, IndexNowService
from mcp_server_indexnow.tools.indexnow import add_indexnow_tools
from mcp_server_indexnow.version import __VERSION__

# Initialize API client and service
indexnow_client = IndexNowApiClient(user_agent=f"mcp-server-indexnow/{__VERSION__}")
indexnow_api_base = os.environ.get(
    "INDEXNOW_API_BASE", "https://api.indexnow.org/indexnow"
)
indexnow_service = IndexNowService(indexnow_api_base, indexnow_client)

# Create MCP instance
mcp = FastMCP("mcp-server-indexnow")

add_indexnow_tools(mcp, indexnow_service)


def app() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    app()
