from . import json_response


async def get_chat(request):
    return json_response({
        "speech": "Barack Hussein Obama II was the 44th and current President of the United States.",
        "displayText": "Barack Hussein Obama II was the 44th and current President of the United States, and the first African American to hold the office. Born in Honolulu, Hawaii, Obama is a graduate of Columbia University   and Harvard Law School, where ",
        "source": "iMobility"
    })
