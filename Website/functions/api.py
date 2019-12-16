import json
from datetime import datetime

import pytz
import requests
from django.conf import settings
from django.db import IntegrityError, transaction


def riot_api(server=None, endpoint=None, version='v4', path=None, session=None):

    url = f'https://{server}.api.riotgames.com/lol/{endpoint}/{version}/{path}'
    headers = {'X-Riot-Token': settings.RIOT_API_KEY}

    response = session.get(url, headers=headers) if session else requests.get(url, headers=headers)

    # TODO: Error Handling

    if response.status_code in [404, 403]:
        return { "error": True, "message": f"{response.status_code} ERROR" }

    return json.loads(json.dumps(response.json()))


def ddragon_api(version=None, method=None, options=None, language='en_US', session=None):

    url = f'https://ddragon.leagueoflegends.com/cdn/{version}/{method}/{language}/{options}'
    headers = {'X-Riot-Token': settings.RIOT_API_KEY}

    response = session.get(url, headers=headers) if session else requests.get(url, headers=headers)

    # TODO: Error Handling

    return json.loads(json.dumps(response.json()))


def get_summoner(summoner_name=None, server=None, summoner_id=None):
    from Website.functions.summoner import save_summoner

    # Build the URL for the Riot API request.
    path = f'summoners/{summoner_id}' if summoner_id else f'summoners/by-name/{summoner_name}'

    # Fetch the information from the Riot API.
    api_response = riot_api(server=server, endpoint='summoner', path=path)

    # Save the Summoner to the database and return the result.
    return save_summoner(api_response, server)


def get_match(game_id=None, server=None):
    from Website.functions.match import save_match

    success = True

    # Build the URL for the Riot API request.
    path = f'matches/{game_id}'

    # Fetch the information from the Riot API.
    api_response = riot_api(server=server, endpoint='match', path=path)

    # Convert the timestamp into a valid DateTime.
    api_response['timestamp'] = datetime.utcfromtimestamp(api_response['gameCreation'] / 1000.).replace(tzinfo=pytz.UTC)

    # Save the Summoner to the database and return the result.
    try:
        with transaction.atomic():
            save_match(api_response, server)

    except IntegrityError as error:
        success = False
        print(error)

    return success


def get_match_list(summoner_id, server='OC1', games=None, fetch_all=False):
    from Website.models import Summoner

    begin_index = 0
    end_index = games if not fetch_all else 100
    next_page = True
    total_matches = []

    # Get the Summoner that you're fetching for.
    summoner_obj = Summoner.objects.get(summoner_id=summoner_id, server=server)

    while next_page:

        # TODO: Make season a variable.
        path = 'matchlists/by-account/' \
               + summoner_obj.account_id \
               + '?season=13&beginIndex=' \
               + str(begin_index) \
               + '&endIndex=' \
               + str(end_index)

        # Get the match list from the Riot API.
        matches = riot_api(server=server, endpoint='match', path=path)

        # Make sure that the matches actually exist in the response.
        if 'matches' in matches:
            total_matches.extend(matches['matches'])

            if len(matches['matches']) != 100 or (len(total_matches) >= games and not fetch_all):
                next_page = False

            begin_index += 100
            end_index += 100
        else:
            next_page = False

    # Return the list of matches.
    return total_matches


def get_latest_version():

    # Fetch list of all versions from the DDragon API.
    version_list = json.loads(json.dumps(requests.get('https://ddragon.leagueoflegends.com/api/versions.json').json()))

    # Return the latest version in the version list.
    return version_list[0]


def get_timeline(match, server):
    from Website.functions.match import save_timeline

    # Build the URL for the Riot API request.
    path = f'timelines/by-match/{match.game_id}'

    # Fetch the information from the Riot API.
    api_response = riot_api(server=server, endpoint='match', path=path)

    # Save the Summoner to the database and return the result.
    return save_timeline(api_response, match)
