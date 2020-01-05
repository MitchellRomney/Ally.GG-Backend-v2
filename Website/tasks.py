from __future__ import absolute_import, unicode_literals

import json
import urllib.parse

from asgiref.sync import async_to_sync
from celery.signals import celeryd_init
from channels.layers import get_channel_layer
from django.template.loader import render_to_string
from django.core.mail import send_mail, get_connection

from AllyBackend.celery import app


@celeryd_init.connect
def startup_tasks(sender=None, conf=None, **kwargs):
    from Website.functions.api import get_latest_version
    from Website.functions.game_data import update_game_data

    # Clean out old queue
    app.control.purge()

    # Update the game data on startup.
    update_game_data(get_latest_version())
    print('Ally is started and ready to receive tasks!')


@app.task
def send_notification(notification_id):
    from Website.models import Notification
    notification_obj = Notification.objects.get(id=notification_id)

    notification = {
        'id': notification_obj.id,
        'title': notification_obj.title,
        'content': notification_obj.content,
        'seen': notification_obj.seen,
        'category': notification_obj.category,
        'dateCreated': str(notification_obj.date_created),
        'dateModified': str(notification_obj.date_modified),
    }

    async_to_sync(get_channel_layer().group_send)(
        f'notifications_{notification_obj.user.id}',
        {
            'type': 'send_notification',
            'message': 'New Notification: ' + str(notification_obj.id),
            'data': {
                'notification': json.dumps(notification)
            }
        }
    )

    return True


@app.task
def update_summoner(summoner_id, server):
    from Website.functions.api import get_summoner

    get_summoner(summoner_id=summoner_id, server=server)

    return True


@app.task
def fetch_match(game_id, summoner_id, server):
    from Website.functions.api import get_match
    from AllyBackend import schema

    get_match(game_id, server)

    query = (
        '''
        {{
          participant(summonerId: "{summoner_id}", server: "{server}", gameId: {game_id}) {{
              id
              position
              champion {{
                  champId
                  name
                  imageFull
              }}
              result
              kills
              deaths
              assists
              match {{
                  gameId
                  queueId
                  queue
                  seasonId
                  mapId
                  gameMode
                  gameType
                  gameVersion
                  gameDuration
                  gameLength
                  timestamp
              }}
              creepScore
              creepScoreAverage
              killParticipation
              kdaAverage
              build {{
                  trinket {{
                      name
                      itemId
                  }}
                  slot1 {{
                      name
                      itemId
                  }}
                  slot2 {{
                      name
                      itemId
                  }}
                  slot3 {{
                      name
                      itemId
                  }}
                  slot4 {{
                      name
                      itemId
                  }}
                  slot5 {{
                      name
                      itemId
                  }}
                  slot6 {{
                      name
                      itemId
                  }}
                  spell1 {{
                      name
                      summonerSpellId
                  }}
                  spell2 {{
                      name
                      summonerSpellId
                  }}
              }}
          }}
        }}
        '''.format(summoner_id=str(summoner_id), game_id=int(game_id), server=str(server))
    )

    result = schema.schema.execute(query)

    async_to_sync(get_channel_layer().group_send)(
        f'summoner-{server}-{summoner_id}',
        {
            'type': 'send_match',
            'message': 'New match added: ' + str(game_id),
            'data': {
                'match': json.dumps(result.data)
            }
        }
    )


@app.task
def save_champions(champions_info):  # Create/Update all champions.
    from Website.models import Champion
    count = 0

    # Loop through champions returned by API and Update/Create.
    for champion, value in champions_info['data'].items():
        count += 1

        Champion.objects.update_or_create(
            key=value['key'],
            defaults={
                'version': value['version'],
                'champ_id': value['id'],
                'name': value['name'],
                'key': value['key'],
                'title': value['title'],
                'blurb': value['blurb'],
                'info_attack': value['info']['attack'],
                'info_defense': value['info']['defense'],
                'info_magic': value['info']['magic'],
                'info_difficulty': value['info']['difficulty'],
                'image_full': value['image']['full'],
                'image_sprite': value['image']['sprite'],
                'image_group': value['image']['group'],
                'image_x': value['image']['x'],
                'image_y': value['image']['y'],
                'image_w': value['image']['w'],
                'image_h': value['image']['h'],
                'tags': value['tags'],
                'partype': value['partype'],
                'stats_hp': value['stats']['hp'],
                'stats_hpperlevel': value['stats']['hpperlevel'],
                'stats_mp': value['stats']['mp'],
                'stats_mpperlevel': value['stats']['mpperlevel'],
                'stats_movespeed': value['stats']['movespeed'],
                'stats_armor': value['stats']['armor'],
                'stats_armorperlevel': value['stats']['armorperlevel'],
                'stats_spellblock': value['stats']['spellblock'],
                'stats_spellblockperlevel': value['stats']['spellblockperlevel'],
                'stats_attackrange': value['stats']['attackrange'],
                'stats_hpregen': value['stats']['hpregen'],
                'stats_hpregenperlevel': value['stats']['hpregenperlevel'],
                'stats_mpregen': value['stats']['mpregen'],
                'stats_mpregenperlevel': value['stats']['mpregenperlevel'],
                'stats_crit': value['stats']['crit'],
                'stats_critperlevel': value['stats']['critperlevel'],
                'stats_attackdamage': value['stats']['attackdamage'],
                'stats_attackdamageperlevel': value['stats']['attackdamageperlevel'],
                'stats_attackspeedperlevel': value['stats']['attackspeedperlevel'],
                'stats_attackspeed': value['stats']['attackspeed'],
            }
        )

    print(f'Champions Updated ({count})')


@app.task
def save_runes(runes_info, version):
    from Website.models import Rune

    # Setup empty Rune.
    Rune.objects.get_or_create(
        rune_id=0,
        name='No Rune'
    )

    count = 0

    # Loop through runes returned by API and Update/Create.
    for tree in runes_info:
        for slot in tree['slots']:
            for rune in slot['runes']:
                count += 1

                Rune.objects.update_or_create(
                    rune_id=rune['id'],
                    defaults={
                        'version': version,
                        'rune_id': rune['id'],
                        'key': rune['key'],
                        'icon': rune['icon'],
                        'name': rune['name'],
                        'short_desc': rune['shortDesc'],
                        'long_desc': rune['longDesc']
                    }
                )

    print(f'Runes Updated ({count})')


@app.task
def save_items(items_info):
    from Website.models import Item

    # Setup empty Item.
    Item.objects.get_or_create(
        item_id=0,
        name='No Item'
    )

    count = 0
    version = items_info['version']

    # Loop through items returned by API and Update/Create.
    for item, value in items_info['data'].items():
        count += 1

        built_into = []
        built_from = []

        if 'into' in value:
            for into_item in value['into']:
                into_item_obj = Item.objects.get_or_create(
                    item_id=into_item,
                    defaults={'item_id': into_item}
                )[0]
                built_into.append(into_item_obj)
        if 'from' in value:
            for from_item in value['from']:
                from_item_obj = Item.objects.get_or_create(
                    item_id=from_item,
                    defaults={'item_id': from_item}
                )[0]
                built_from.append(from_item_obj)

        defaults = {
            'version': version,
            'item_id': item,
            'name': value['name'],
            'description': value['description'],
            'colloq': value['colloq'],
            'plaintext': value['plaintext'],
            'image_full': value['image']['full'],
            'image_sprite': value['image']['sprite'],
            'image_group': value['image']['group'],
            'image_x': value['image']['x'],
            'image_y': value['image']['y'],
            'image_w': value['image']['w'],
            'image_h': value['image']['h'],
            'gold_base': value['gold']['base'],
            'gold_purchasable': value['gold']['purchasable'],
            'gold_total': value['gold']['total'],
            'gold_sell': value['gold']['sell'],
        }

        field_mappings = {
            'consumed': 'consumed',
            'stacks': 'stacks',
            'depth': 'depth',
            'consumeOnFull': 'consume_on_full',
            'specialRecipe': 'special_recipe',
            'inStore': 'in_store',
            'hideFromAll': 'hide_from_all',
            'requiredChampion': 'required_champion',
            'requiredAlly': 'required_ally',
            'tags': 'tags',
            '1': 'maps_1',
            '8': 'maps_8',
            '10': 'maps_10',
            '11': 'maps_11',
            '12': 'maps_12',
            'FlatHPPoolMod': 'flat_hp_pool_mod',
            'rFlatHPModPerLevel': 'r_flat_hp_mod_per_level',
            'FlatMPPoolMod': 'flat_mp_pool_mod',
            'rFlatMPModPerLevel': 'r_flat_mp_mod_per_level',
            'PercentHPPoolMod': 'percent_hp_pool_mod',
            'PercentMPPoolMod': 'percent_mp_pool_mod',
            'FlatHPRegenMod': 'flat_hp_regen_mod',
            'rFlatHPRegenModPerLevel': 'r_flat_hp_regen_mod_per_level',
            'PercentHPRegenMod': 'percent_hp_regen_mod',
            'FlatMPRegenMod': 'flat_mp_regen_mod',
            'rFlatMPRegenModPerLevel': 'r_flat_mp_regen_mod_per_level',
            'PercentMPRegenMod': 'percent_mp_regen_mod',
            'FlatArmorMod': 'flat_armor_mod',
            'rFlatArmorModPerLevel': 'r_flat_armor_mod_per_level',
            'PercentArmorMod': 'percent_armor_mod',
            'rFlatArmorPenetrationMod': 'r_flat_armor_penetration_mod',
            'rFlatArmorPenetrationModPerLevel': 'r_flat_armor_penetration_mod_per_level',
            'rPercentArmorPenetrationMod': 'r_percent_armor_penetration_mod',
            'rPercentArmorPenetrationModPerLevel': 'r_percent_armor_penetration_mod_per_level',
            'FlatPhysicalDamageMod': 'flat_physical_damage_mod',
            'rFlatPhysicalDamageModPerLevel': 'r_flat_physical_damage_mod_per_level',
            'PercentPhysicalDamageMod': 'percent_physical_damage_mod',
            'FlatMagicDamageMod': 'flat_magic_damage_mod',
            'rFlatMagicDamageModPerLevel': 'r_flat_magic_damage_mod_per_level',
            'PercentMagicDamageMod': 'percent_magic_damage_mod',
            'FlatMovementSpeedMod': 'flat_movement_speed_mod',
            'rFlatMovementSpeedModPerLevel': 'r_flat_movement_speed_mod_per_level',
            'PercentMovementSpeedMod': 'percent_movement_speed_mod',
            'rPercentMovementSpeedModPerLevel': 'r_percent_movement_speed_mod_per_level',
            'FlatAttackSpeedMod': 'flat_attack_speed_mod',
            'PercentAttackSpeedMod': 'percent_attack_speed_mod',
            'rPercentAttackSpeedModPerLevel': 'r_percent_attack_speed_mod_per_level',
            'rFlatDodgeMod': 'r_flat_dodge_mod',
            'rFlatDodgeModPerLevel': 'r_flat_dodge_mod_per_level',
            'PercentDodgeMod': 'percent_dodge_mod',
            'FlatCritChanceMod': 'flat_crit_chance_mod',
            'rFlatCritChanceModPerLevel': 'r_flat_crit_chance_mod_per_level',
            'PercentCritChanceMod': 'percent_crit_chance_mod',
            'FlatCritDamageMod': 'flat_crit_damage_mod',
            'rFlatCritDamageModPerLevel': 'r_flat_crit_damage_mod_per_level',
            'PercentCritDamageMod': 'percent_crit_damage_mod',
            'FlatBlockMod': 'flat_block_mod',
            'PercentBlockMod': 'percent_block_mod',
            'FlatSpellBlockMod': 'flat_spell_block_mod',
            'rFlatSpellBlockModPerLevel': 'r_flat_spell_block_mod_per_level',
            'PercentSpellBlockMod': 'percent_spell_block_mod',
            'FlatEXPBonus': 'flat_exp_bonus',
            'PercentEXPBonus': 'percent_exp_bonus',
            'rPercentCooldownMod': 'r_percent_cooldown_mod',
            'rPercentCooldownModPerLevel': 'r_percent_cooldown_mod_per_level',
            'rFlatTimeDeadMod': 'r_flat_time_dead_mod',
            'rFlatTimeDeadModPerLevel': 'r_flat_time_dead_mod_per_level',
            'rPercentTimeDeadMod': 'r_percent_time_dead_mod',
            'rPercentTimeDeadModPerLevel': 'r_percent_time_dead_mod_per_level',
            'rFlatGoldPer10Mod': 'r_flat_gold_per10_mod',
            'rFlatMagicPenetrationMod': 'r_flat_magic_penetration_mod',
            'rFlatMagicPenetrationModPerLevel': 'r_flat_magic_penetration_mod_per_level',
            'rPercentMagicPenetrationMod': 'r_percent_magic_penetration_mod',
            'rPercentMagicPenetrationModPerLevel': 'r_percent_magic_penetration_mod_per_level',
            'FlatEnergyRegenMod': 'flat_energy_regen_mod',
            'rFlatEnergyRegenModPerLevel': 'r_flat_energy_regen_mod_per_level',
            'FlatEnergyPoolMod': 'flat_energy_pool_mod',
            'rFlatEnergyModPerLevel': 'r_flat_energy_mod_per_level',
            'PercentLifeStealMod': 'percent_life_steal_mod',
            'PercentSpellVampMod': 'percent_spell_vamp_mod',
        }

        for field in value:
            if field in field_mappings:
                defaults[field_mappings[field]] = value[field]
            for image_field in value['image']:
                if image_field in field_mappings:
                    defaults[field_mappings[image_field]] = value['image'][image_field]
            for gold_field in value['gold']:
                if gold_field in field_mappings:
                    defaults[field_mappings[gold_field]] = value['gold'][gold_field]
            for maps_field in value['maps']:
                if maps_field in field_mappings:
                    defaults[field_mappings[maps_field]] = value['maps'][maps_field]
            for stats_field in value['stats']:
                if stats_field in field_mappings:
                    defaults[field_mappings[stats_field]] = value['stats'][stats_field]

        obj, created = Item.objects.update_or_create(
            item_id=item,
            defaults=defaults
        )

        obj.built_into.set(built_into)
        obj.built_from.set(built_from)

    print(f'Items Updated ({count})')


@app.task
def save_spells(spells_info):
    from Website.models import SummonerSpell

    # Setup empty Item.
    SummonerSpell.objects.get_or_create(
        key=0,
        name='No Summoner Spell'
    )

    count = 0
    version = spells_info['version']

    for spell, value in spells_info['data'].items():
        count += 1

        defaults = {
                'version': version,
                'key': value['key'],
                'summoner_spell_id': value['id'],
                'name': value['name'],
                'description': value['description'],
                'tooltip': value['tooltip'],
                'maxrank': value['maxrank'],
                'cooldown_burn': value['cooldownBurn'],
                'cost_burn': value['costBurn'],
                'summoner_level': value['summonerLevel'],
                'cost_type': value['costType'],
                'maxammo': value['maxammo'],
                'range_burn': value['rangeBurn'],
                'image_full': value['image']['full'],
                'image_sprite': value['image']['sprite'],
                'image_group': value['image']['group'],
                'image_x': value['image']['x'],
                'image_y': value['image']['y'],
                'image_w': value['image']['w'],
                'image_h': value['image']['h'],
                'resource': value['resource'] if 'resource' in value else None,
                'cooldown': value['cooldown'][0],
                'cost': value['cost'][0],
                'range': value['range'][0]
            }

        SummonerSpell.objects.update_or_create(
            key=value['key'],
            defaults=defaults
        )

    print(f'Spells Updated ({count})')


@app.task
def send_early_access_email(payload):
    content = {
        'name': payload["name"],
        'email': urllib.parse.quote(payload["email"], safe=''),
        'domain': 'ally.gg',
        'key': urllib.parse.quote(payload["key"], safe=''),
    }

    send_mail(
        'Congratulations! You\'ve been accepted into the Ally.gg Alpha!',
        render_to_string('Website/email/alpha_access.txt', content),
        'noreply@ally.gg',
        [payload["email"], ],
        html_message=render_to_string('Website/email/alpha_access.html', content)
    )

