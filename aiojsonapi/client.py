"""Module with API client. Provides convenient way of handling exceptions."""

import json

import aiohttp

from aiojsonapi.exception import ApiException


class ApiClient:
    """Base API client class."""

    error_field_name = "error"
    error_text_field = "reason"
    result_wrapped_in_field = "result"

    def __init__(
        self,
        server_ip,
        server_port=None,
        https=True,
        json_decoder=json.JSONDecoder,
        json_encoder=json.JSONEncoder,
    ):
        self.server_ip = server_ip
        self.server_port = server_port
        self.protocol = "https" if https else "http"
        self.json_decoder = json_decoder
        self.json_encoder = json_encoder

    @staticmethod
    def _delete_none(request: dict):
        """Removes None values from request."""

        return {key: value for key, value in request.items() if value is not None}

    def _format_path(self, endpoint):
        url = f"{self.protocol}://{self.server_ip}"
        if self.server_port:
            url += f":{self.server_port}"
        url += f"/{endpoint}"
        return url

    async def _make_request(self, endpoint, method, json_data=None, keep_none=False, headers=None):
        url = self._format_path(endpoint)
        data = self._delete_none(json_data or {}) if not keep_none else json_data or {}
        async with aiohttp.ClientSession() as session:
            _method = getattr(session, method)
            async with _method(
                url, data=json.dumps(data, cls=self.json_encoder), headers=headers
            ) as response:
                body = await response.text()
                result = json.loads(body, cls=self.json_decoder)
                if self.error_field_name in result:
                    raise ApiException(result.get(self.error_text_field))
                if self.result_wrapped_in_field:
                    return result[self.result_wrapped_in_field]
                return result

    async def get(self, endpoint, json_data=None, keep_none=False, headers=None):
        """Sends GET request to API."""

        return await self._make_request(
            endpoint, "get", json_data=json_data, keep_none=keep_none, headers=headers
        )

    async def post(self, endpoint, json_data=None, keep_none=False, headers=None):
        """Sends POST request to API."""

        return await self._make_request(
            endpoint, "post", json_data=json_data, keep_none=keep_none, headers=headers
        )

    async def delete(self, endpoint, json_data=None, keep_none=False, headers=None):
        """Sends DELETE request to API."""

        return await self._make_request(
            endpoint,
            "delete",
            json_data=json_data,
            keep_none=keep_none,
            headers=headers,
        )

    async def put(self, endpoint, json_data=None, keep_none=False, headers=None):
        """Sends PUT request to API."""

        return await self._make_request(
            endpoint, "put", json_data=json_data, keep_none=keep_none, headers=headers
        )

    async def patch(self, endpoint, json_data=None, keep_none=False, headers=None):
        """Sends PATCH request to API."""

        return await self._make_request(
            endpoint, "patch", json_data=json_data, keep_none=keep_none, headers=headers
        )
