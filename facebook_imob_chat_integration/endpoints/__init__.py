import json
import uuid
from functools import partial

import ujson

import apiai
from aiohttp.web_request import Request
from aiohttp.web_response import json_response, Response
from facebook_imob_chat_integration.endpoints import chat
from facebook_imob_chat_integration.endpoints.chat import get_chat_routing

from . import version, status

json_response = partial(json_response, dumps=ujson.dumps)

ai = apiai.ApiAI('c12e662bfe8d4cd39a60626541ae9c24')

async def analyze(request: Request) -> Response:
    params = dict(request.query)
    ai_request = ai.text_request()
    ai_request.lang = 'de'
    ai_request.session_id = str(uuid.uuid4())
    ai_request.query = params['query']
    ai_response = ai_request.getresponse()
    content = json.loads(ai_response.read().decode())
    if content['result']['action'] == 'routing':
        from_location_query = content['result']['parameters']['LocationFrom']
        to_location_query = content['result']['parameters']['LocationTo']
        return await get_chat_routing(request, from_location_query, to_location_query)
    else:
        return json_response(content)


ROUTES = {
    ('GET', '/version', version.get_version),
    ('GET', '/status', status.get_status),
    ('GET', '/facebook_chat', chat.get_chat),
    ('GET', '/analyze', analyze),
    ('POST', '/facebook_chat', chat.get_chat),
}
