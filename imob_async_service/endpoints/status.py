from . import json_response


async def get_status(request):
    return json_response({
        'status': 'OK',
    })
