"""Module with middlewares."""

import json

from aiohttp import web


def json_error(message, code, status):
    """Returns error in JSON format."""

    return web.Response(
        body=json.dumps({"error": True, "reason": {"text": message, "code": code}}).encode(
            "utf-8"
        ),
        content_type="application/json",
        status=status,
    )


async def error_middleware(app, handler):
    """Middleware for 404 error handling. Returns result in JSON format."""

    async def middleware_handler(request):
        try:
            response = await handler(request)
            if response.status == 404:
                return json_error(response.message, "NotFound", response.status)
            return response
        except web.HTTPException as ex:
            if ex.status == 404:
                return json_error(ex.reason, "NotFound", ex.status)
            raise ex

    return middleware_handler
