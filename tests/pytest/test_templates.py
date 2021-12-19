import typing

import aiohttp.web
import pytest

from aiojsonapi import exception, routes
from aiojsonapi.template import JSONTemplate


@pytest.mark.parametrize(
    "method", [routes.get, routes.post, routes.patch, routes.put, routes.delete]
)
async def test_good(aiohttp_client, method):
    routes.routes._items.clear()

    @method("/test")
    @JSONTemplate({"interface": str})
    async def test(request):
        return {"interfaces": [request.validated_data["interface"]]}

    app = aiohttp.web.Application()
    app.router.add_routes(routes.routes)
    client = await aiohttp_client(app)
    resp = await getattr(client, method.__name__)("/test", json={"interface": "en2"})
    body = await resp.json()
    assert {"error": False, "result": {"interfaces": ["en2"]}} == body
    assert resp.status == 200


@pytest.mark.parametrize(
    "method", [routes.get, routes.post, routes.patch, routes.put, routes.delete]
)
async def test_missing_data(aiohttp_client, method):
    routes.routes._items.clear()

    @method("/test")
    @JSONTemplate({"interface": str})
    async def test(request):
        return {"interfaces": [request.validated_data["interface"]]}

    app = aiohttp.web.Application()
    app.router.add_routes(routes.routes)
    client = await aiohttp_client(app)
    resp = await getattr(client, method.__name__)("/test", json={"interfaces": "en2"})
    assert resp.status == 400
    body = await resp.json()
    assert {
        "error": True,
        "reason": {
            "text": exception.DataMissing.text,
            "path": "interface",
            "code": exception.DataMissing.__name__,
        },
    } == body


@pytest.mark.parametrize(
    "method", [routes.get, routes.post, routes.patch, routes.put, routes.delete]
)
async def test_unknown_fields(aiohttp_client, method):
    routes.routes._items.clear()

    @method("/test")
    @JSONTemplate({"interface": str}, ignore_unknown=False)
    async def test(request):
        return {"interfaces": [request.validated_data["interface"]]}

    app = aiohttp.web.Application()
    app.router.add_routes(routes.routes)
    client = await aiohttp_client(app)
    resp = await getattr(client, method.__name__)(
        "/test", json={"interface": "en2", "test": True, "test2": False}
    )
    assert resp.status == 400
    body = await resp.json()
    assert {
        "error": True,
        "reason": {
            "text": exception.UnknownFields.text,
            "path": ["test", "test2"],
            "code": exception.UnknownFields.__name__,
        },
    } == body


@pytest.mark.parametrize(
    "method", [routes.get, routes.post, routes.patch, routes.put, routes.delete]
)
async def test_unknown_fields(aiohttp_client, method):
    routes.routes._items.clear()

    @method("/test")
    @JSONTemplate(
        {"interface": int, "test": typing.Optional[int]},
        ignore_unknown=False,
    )
    async def test(request):
        return {"interfaces": [request.validated_data["interface"]]}

    app = aiohttp.web.Application()
    app.router.add_routes(routes.routes)
    client = await aiohttp_client(app)
    resp = await getattr(client, method.__name__)(
        "/test",
        json={
            "interface": ["en2"],
        },
    )
    assert resp.status == 400
    body = await resp.json()
    assert {
        "error": True,
        "reason": {
            "text": exception.WrongDataType.text,
            "path": "interface",
            "code": exception.WrongDataType.__name__,
        },
    } == body


@pytest.mark.parametrize(
    "method", [routes.get, routes.post, routes.patch, routes.put, routes.delete]
)
async def test_unknown_optional(aiohttp_client, method):
    routes.routes._items.clear()

    @method("/test")
    @JSONTemplate(
        {"interface": str, "test": typing.Optional[int]},
        ignore_unknown=False,
    )
    async def test(request):
        return {"interfaces": [request.validated_data["interface"]]}

    app = aiohttp.web.Application()
    app.router.add_routes(routes.routes)
    client = await aiohttp_client(app)
    resp = await getattr(client, method.__name__)(
        "/test",
        json={
            "interface": "en2",
        },
    )
    assert resp.status == 200
    body = await resp.json()
    assert {"error": False, "result": {"interfaces": ["en2"]}} == body
