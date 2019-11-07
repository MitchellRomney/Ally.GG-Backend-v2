from Website.models import Summoner


def save_summoner(summoner_data, server):
    defaults = {}
    field_mappings = {
        'id': 'summoner_id',
        'accountId': 'account_id',
        'puuid': 'puuid',
        'name': 'summoner_name',
        'profileIconId': 'profile_icon_id',
        'summonerLevel': 'summoner_level'
    }

    for field in summoner_data:
        if field in field_mappings:
            defaults[field_mappings[field]] = summoner_data[field]

    obj, created = Summoner.objects.update_or_create(
        summoner_id=summoner_data['id'],
        server=server,
        defaults=defaults
    )

    return {
        'summoner': obj,
        'created': created
    }
