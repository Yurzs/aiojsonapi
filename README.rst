aiojsonapi
==========
|pipeline status| |coverage report| |pypi link|

.. |coverage report| image:: https://git.yurzs.dev/yurzs/aiojson/badges/master/coverage.svg
   :target: https://git.yurzs.dev/yurzs/aiojson/-/commits/master

.. |pipeline status| image:: https://git.yurzs.dev/yurzs/aiojson/badges/master/pipeline.svg
   :target: https://git.yurzs.dev/yurzs/aiojson/-/commits/master

.. |pypi link| image:: https://badge.fury.io/py/aiojson.svg
   :target: https://pypi.org/project/aiojsonapi

Aiohttp API constructor with dataclass based request validation.

Usage
-----

Simple example:

.. code-block:: python

    import typing

    from aiojsonapi import JSONTemplate


    @JSONTemplate({
        "messages": [{
            "id": int,
            "text": typing.Optional[str]
    }])
    async def received_message(request):
        pass
