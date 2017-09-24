from .. import __version__, __project__, __revision__
from . import json_response


async def get_version(request):
    return json_response({
        'version': __version__,
        'project': __project__,
        'revision': __revision__,
        'x-request-id': request.headers.get('X-Request-Id')
    })
