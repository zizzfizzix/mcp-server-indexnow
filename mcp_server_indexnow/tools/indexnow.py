from typing import Any, Dict, List

from mcp.server.fastmcp import FastMCP

from mcp_server_indexnow.services.indexnow import IndexNowService


def add_indexnow_tools(mcp: FastMCP, indexnow_service: IndexNowService) -> None:
    @mcp.tool()
    async def submit_urls(
        urls: List[str],
        key: str | None = None,
        host: str | None = None,
        key_location: str | None = None,
    ) -> Dict[str, Any]:
        """Submit one or more URLs to search engines using the IndexNow protocol.

        Args:
            urls: List of URLs to submit
                  (e.g. ["https://example.com/page1", "https://example.com/page2"])
            key: Your IndexNow secret key
                 (optional if INDEXNOW_SECRET_KEY env var is set)
            host: The host of your website
                  (e.g. \"example.com\", required if submitting multiple URLs and it
                   cannot be inferred from the first URL, or if submitting an
                   empty list)
            key_location: Optional location of your key file
                          (e.g. "https://example.com/key.txt")

        Returns:
            A dictionary containing the result of the submission:
            {"status": 200, "message": "OK"}
            {"status": 202, "message": "Accepted"}
            {"status": 4xx/5xx, "error": "Error description"}
        """
        result = await indexnow_service.submit_urls(urls, key, host, key_location)

        return result
