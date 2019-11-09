import requests
from Website.functions.api import ddragon_api


def update_game_data(version):
    from Website.tasks import save_champions, save_items, save_runes, save_spells

    with requests.session() as session:

        # Fetch all current Champion information from DDragon API.
        save_champions.delay(ddragon_api(version=version, method='data', options='champion.json', session=session))

        # Fetch all current Rune information from DDragon API.
        save_runes.delay(ddragon_api(version=version, method='data', options='runesReforged.json', session=session), version)

        # Fetch all current Item information from DDragon API.
        save_items.delay(ddragon_api(version=version, method='data', options='item.json', session=session))

        # Fetch all current Summoner Spell information from DDragon API.
        save_spells.delay(ddragon_api(version=version, method='data', options='summoner.json', session=session))

    set_ranked_tiers()


def set_ranked_tiers():
    from Website.models import RankedTier
    RankedTier.objects.get_or_create(key='CHALLENGER', name='Challenger', order=1)
    RankedTier.objects.get_or_create(key='GRANDMASTER', name='Grandmaster', order=2)
    RankedTier.objects.get_or_create(key='MASTER', name='Master', order=3)
    RankedTier.objects.get_or_create(key='DIAMOND', name='Diamond', order=4)
    RankedTier.objects.get_or_create(key='PLATINUM', name='Platinum', order=5)
    RankedTier.objects.get_or_create(key='GOLD', name='Gold', order=6)
    RankedTier.objects.get_or_create(key='SILVER', name='Silver', order=7)
    RankedTier.objects.get_or_create(key='BRONZE', name='Bronze', order=8)
    RankedTier.objects.get_or_create(key='IRON', name='Iron', order=9)
