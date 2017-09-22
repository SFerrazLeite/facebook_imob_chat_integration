from functools import partial

import ujson

from aiohttp.web_response import json_response
from imob_async_service.endpoints import chat

from . import version, status

json_response = partial(json_response, dumps=ujson.dumps)


ROUTES = {
    ('GET', '/version', version.get_version),
    ('GET', '/status', status.get_status),
    ('GET', '/facebook_chat', chat.get_chat),
}
