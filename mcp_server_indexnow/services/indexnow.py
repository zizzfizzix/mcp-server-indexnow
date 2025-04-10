import os
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import urlparse

import httpx


class IndexNowApiClient:
    def __init__(self, user_agent: str):
        self.user_agent = user_agent

    async def send_post_request(
        self, url: str, data: Dict[str, Any]
    ) -> Tuple[int, Union[Dict[str, Any], None]]:
        """Make a POST request to the IndexNow API."""
        headers = {
            "User-Agent": self.user_agent,
            "Content-Type": "application/json; charset=utf-8",
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url, headers=headers, json=data, timeout=30.0
                )
                # Don't raise_for_status here, we want to handle specific codes
                try:
                    response_json = response.json()
                except Exception:
                    response_json = None  # No JSON body expected for some statuses
                return response.status_code, response_json
            except httpx.RequestError as e:
                return 500, {"error": f"Request failed: {e}"}
            except Exception as e:
                # Catch other potential errors during request sending
                return 500, {"error": f"An unexpected error occurred: {e}"}

    async def send_get_request(
        self, url: str, params: Dict[str, Any]
    ) -> Tuple[int, Union[Dict[str, Any], None]]:
        """Make a GET request to the IndexNow API."""
        headers = {"User-Agent": self.user_agent}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    url, headers=headers, params=params, timeout=30.0
                )
                # Don't raise_for_status here
                try:
                    response_json = response.json()
                except Exception:
                    response_json = None
                return response.status_code, response_json
            except httpx.RequestError as e:
                return 500, {"error": f"Request failed: {e}"}
            except Exception as e:
                return 500, {"error": f"An unexpected error occurred: {e}"}


class IndexNowService:
    def __init__(self, api_base: str, api_client: IndexNowApiClient):
        self.api_base = api_base
        self.api_client = api_client
        self.default_key = os.environ.get("INDEXNOW_SECRET_KEY")

    def _get_key_or_error(
        self, key: Optional[str]
    ) -> Union[str, Dict[str, Union[str, int]]]:
        """Get the key from param or env var, returning an error dict if none."""
        key_to_use = key or self.default_key
        if key_to_use is None:
            return {
                "status": 400,  # Use a generic client error code
                "error": (
                    "No secret key provided and INDEXNOW_SECRET_KEY "
                    "environment variable not set"
                ),
            }
        return key_to_use

    def _get_host_or_error(
        self, host: Optional[str], urls: List[str]
    ) -> Union[str, Dict[str, Union[str, int]]]:
        """Determine host from param or URLs, returning an error dict if none."""
        if host:
            return host
        if urls:
            parsed_host = urlparse(urls[0]).netloc
            if parsed_host:
                return parsed_host
            else:
                return {
                    "status": 400,
                    "error": "Could not determine host from the first URL",
                }
        return {"status": 400, "error": "Host must be provided if URL list is empty"}

    def _handle_response(
        self, status_code: int, response_body: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Interpret IndexNow API response codes."""
        if status_code == 200:
            return {"status": 200, "message": "OK"}
        elif status_code == 202:
            return {"status": 202, "message": "Accepted"}
        elif status_code == 400:
            return {"status": 400, "error": "Bad Request (Invalid format)"}
        elif status_code == 403:
            return {"status": 403, "error": "Forbidden (Invalid key)"}
        elif status_code == 422:
            return {
                "status": 422,
                "error": "Unprocessable Entity (URL does not belong to host)",
            }
        elif status_code == 429:
            return {"status": 429, "error": "Too Many Requests"}
        elif response_body and "error" in response_body:
            # Handle errors reported by the client itself (e.g., connection error)
            return {"status": status_code or 500, "error": response_body["error"]}
        else:
            return {
                "status": status_code,
                "error": f"Received unexpected HTTP status code {status_code}",
            }

    async def submit_urls(
        self,
        urls: List[str],
        key: str | None = None,
        host: str | None = None,
        key_location: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Submit one or more URLs to IndexNow API."""
        if not urls:
            return {"status": 400, "error": "URL list cannot be empty"}

        key_result = self._get_key_or_error(key)
        if isinstance(key_result, dict):
            return key_result
        actual_key = key_result

        host_result = self._get_host_or_error(host, urls)
        if isinstance(host_result, dict):
            return host_result
        actual_host = host_result

        if len(urls) == 1:
            # Use GET for single URL submission
            params = {"url": urls[0], "key": actual_key}
            # Only include keyLocation if explicitly provided for GET
            if key_location:
                params["keyLocation"] = key_location

            status_code, response_body = await self.api_client.send_get_request(
                self.api_base, params
            )
        else:
            # Use POST for multiple URLs
            data = {
                "host": actual_host,
                "key": actual_key,
                "urlList": urls,
            }
            # Include default key location if not provided
            data["keyLocation"] = (
                key_location or f"https://{actual_host}/{actual_key}.txt"
            )

            status_code, response_body = await self.api_client.send_post_request(
                self.api_base, data
            )

        return self._handle_response(status_code, response_body)
