import arrow
from aiohttp import ClientError
from aiohttp.web_request import Request

from . import json_response


async def get_chat(request):
    body = await request.json()
    from_location_query = body['result']['parameters']['LocationFrom']
    to_location_query = body['result']['parameters']['LocationTo']
    return await get_chat_routing(request, from_location_query, to_location_query)

async def get_chat_routing(request, from_location_query, to_location_query):
    try:
        from_location = await _fetch_location(request, from_location_query)
    except ClientError:
        return json_response({
            "speech": "Tut mir leid. Da ist was schief gegangen.",
            "source": "iMobility"
        })
    if not from_location:
        return json_response({
            "speech": "Ich habe den Abfahrtsort {} leider nicht gefunden :(".format(from_location_query),
            "source": "iMobility"
        })

    try:
        to_location = await _fetch_location(request, to_location_query)
    except ClientError:
        return json_response({
            "speech": "Tut mir leid. Da ist was schief gegangen.",
            "source": "iMobility"
        })
    if not to_location:
        return json_response({
            "speech": "Ich habe den Zielort {} leider nicht gefunden :(".format(to_location_query),
            "source": "iMobility"
        })
    try:
        journey = await _fetch_journey(request, from_location, to_location)
    except ClientError:
        return json_response({
            "speech": "Tut mir leid. Da ist was schief gegangen.",
            "source": "iMobility"
        })
    if not journey:
        return json_response({
            "speech": "Ich habe leider keine Verbindung von {} nach {} gefunden.".format(from_location_query,
                                                                                         to_location_query),
            "source": "iMobility"
        })
    transfers = journey.get('transfers', 0)
    if transfers == 0:
        umstiege = 'nicht'
    else:
        umstiege = "{}x".format(transfers)
    first_bubble = "Für deinen Weg brauchst du {} Minuten und musst {} umsteigen".format(journey['duration'], umstiege)

    relevant_sections = _extract_sections(journey)

    transport = relevant_sections[0]['transport']
    departure_location_name = relevant_sections[0]['departure']['location']['name']
    second_bubble = "Nimm bei {} um {} {} {} Richtung {}.".format(
        departure_location_name,
        arrow.get(relevant_sections[0]['departure']['datetime']).to('local').format("HH:mm"),
        _get_sumbeans_string(transport),
        transport['line']['name'],
        transport['direction'],
    )

    intermediate_bubbles = []
    for section in relevant_sections[1:-1]:
        transport = section['transport']
        departure_location_name = section['departure']['location']['name']
        intermediate_bubbles.append("Steige bei {} um in {} {} Richtung {}".format(
            departure_location_name,
            _get_sumbeans_string(transport),
            transport['line']['name'],
            transport['direction'],
        )
        )
    if relevant_sections[-1]['transport']['means'] == 'public':
        last_bubble = ""
        if len(relevant_sections) > 1:
            transport = relevant_sections[-1]['transport']
            departure_location_name = relevant_sections[-1]['departure']['location']['name']
            last_bubble += "Steige bei {} um in {} {} Richtung {}\n".format(
                departure_location_name,
                _get_sumbeans_string(transport),
                transport['line']['name'],
                transport['direction'],
            )
        last_bubble += "Nach {} Minuten hast du {} erreicht.".format(
            relevant_sections[-1]['duration'],
            relevant_sections[-1]['arrival']['location']['name']
        )
    else:
        last_bubble = "Von {} sind es noch {} Minuten zu Fuß.".format(
            relevant_sections[-1]['departure']['location']['name'],
            relevant_sections[-1]['duration'],
        )

    speech = first_bubble + "\n" + second_bubble
    for bubble in intermediate_bubbles:
        speech += "\n" + bubble
    speech += "\n" + last_bubble

    return json_response({
        "speech": speech,
        "source": "iMobility"
    })


async def _fetch_location(request: Request, query: str):
    url = request.app['config']['IMOB_API_URL'] + '/routing/api/v2/locations'
    response = await request.app['client'].get(url, params={'query': query})
    if response.status > 399:
        raise ClientError()

    body = await response.json()

    if not body.get('data'):
        return None

    return body['data'][0]


async def _fetch_journey(request: Request, from_location, to_location):
    url = request.app['config']['IMOB_API_URL'] + '/routing/api/v2/journeys'
    params = {
        'start_location_id': from_location['id'],
        'destination_location_id': to_location['id'],
        'departure': arrow.get().isoformat()
    }
    response = await request.app['client'].get(url, params=params)
    if response.status > 399:
        raise ClientError()
    body = await response.json()

    if not body.get('data'):
        return None
    if not body['data'].get('transportation_groups'):
        return None
    if not body['data']['transportation_groups'].get('resolved'):
        return None
    first_resolved = body['data']['transportation_groups']['resolved'][0]
    if not first_resolved.get('group') == 'public':
        return None
    if not first_resolved.get('journeys'):
        return None
    return first_resolved['journeys'][0]


def _extract_sections(journey):
    sections = []
    if journey.get('first_miles'):
        sections += journey['first_miles'][0]['sections']
    sections += journey['main_leg']['sections']
    if journey.get('last_miles'):
        sections += journey['last_miles'][0]['sections']
    while sections[0].get('transport', {}).get('means') == 'walk':
        sections.pop(0)
    sections = [section for section in sections if section['transport']['means'] != 'transfer']
    sections = [section for section in sections[0:-1] if section['transport']['means'] != 'walk'] + [sections[-1]]
    return sections


def _get_sumbeans_string(transport):
    sub_means = transport.get('sub_means')
    if not sub_means:
        return ""
    return {
        'city_bus': "den Bus",
        'city_train': "die Bahn",
        'express_bus': "den Bus",
        'metro': "die",
        'regional_bus': "den Bus",
        's_bahn': "die S-Bahn",
        'train': "den Zug",
        'tram': "die Bim"
    }.get(sub_means, "das Verkehrsmittel")
