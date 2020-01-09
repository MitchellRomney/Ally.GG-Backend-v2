def save_summoner(summoner_data, server):
    from Website.models import Summoner
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


def update_summoner(summoner_id, server='OC1'):
    from Website.models import Summoner, RankedTier
    from Website.functions.api import riot_api
    from django.utils import timezone

    # Get the Summoner you're trying to update.
    summoner = Summoner.objects.get(summoner_id=summoner_id)

    # Set the date_updated field to now.
    summoner.date_updated = timezone.now()

    # Save the Summoner. This all happens immediately so the update summoner script doesn't pick it up twice.
    summoner.save()

    # Fetch the Summoner information from the Riot API.
    summoner_info = riot_api(server, 'summoner', 'v4', 'summoners/' + summoner_id)

    # Update basic Summoner information.
    summoner.summoner_name = summoner_info['name']
    summoner.profile_icon_id = summoner_info['profileIconId']
    summoner.summoner_level = summoner_info['summonerLevel']

    # Fetch the Summoner Ranked information from the Riot API.
    ranked_info = riot_api(server, 'league', 'v4', 'entries/by-summoner/' + summoner.summoner_id)

    # Iterate through the different Ranked Queues.
    for queue in ranked_info:

        # If the Summoner is ranked in SoloQ, update the SoloQ information.
        if queue['queueType'] == 'RANKED_SOLO_5x5':
            summoner.ranked_solo_league_id = queue['leagueId']
            summoner.ranked_solo_tier = RankedTier.objects.get(key=queue['tier'])
            summoner.ranked_solo_hot_streak = queue['hotStreak']
            summoner.ranked_solo_wins = queue['wins']
            summoner.ranked_solo_losses = queue['losses']
            summoner.ranked_solo_veteran = queue['veteran']
            summoner.ranked_solo_rank = queue['rank']
            summoner.ranked_solo_inactive = queue['inactive']
            summoner.ranked_solo_fresh_blood = queue['freshBlood']
            summoner.ranked_solo_league_points = queue['leaguePoints']

        # If the Summoner is ranked in FlexQ, update the FlexQ information.
        elif queue['queueType'] == 'RANKED_FLEX_SR':
            summoner.ranked_flex_sr_league_id = queue['leagueId']
            summoner.ranked_flex_sr_tier = RankedTier.objects.get(key=queue['tier'])
            summoner.ranked_flex_sr_hot_streak = queue['hotStreak']
            summoner.ranked_flex_sr_wins = queue['wins']
            summoner.ranked_flex_sr_losses = queue['losses']
            summoner.ranked_flex_sr_veteran = queue['veteran']
            summoner.ranked_flex_sr_rank = queue['rank']
            summoner.ranked_flex_sr_inactive = queue['inactive']
            summoner.ranked_flex_sr_fresh_blood = queue['freshBlood']
            summoner.ranked_flex_sr_league_points = queue['leaguePoints']

        # If the Summoner is ranked in 3v3, update the 3v3 information.
        elif queue['queueType'] == 'RANKED_FLEX_TT':
            summoner.ranked_flex_tt_league_id = queue['leagueId']
            summoner.ranked_flex_tt_tier = RankedTier.objects.get(key=queue['tier'])
            summoner.ranked_flex_tt_hot_streak = queue['hotStreak']
            summoner.ranked_flex_tt_wins = queue['wins']
            summoner.ranked_flex_tt_losses = queue['losses']
            summoner.ranked_flex_tt_veteran = queue['veteran']
            summoner.ranked_flex_tt_rank = queue['rank']
            summoner.ranked_flex_tt_inactive = queue['inactive']
            summoner.ranked_flex_tt_fresh_blood = queue['freshBlood']
            summoner.ranked_flex_tt_league_points = queue['leaguePoints']

    # Save the newly updated Summoner.
    summoner.save()

