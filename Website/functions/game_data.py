from Website.functions.api import ddragon_api
from Website.models import Champion, Item, Rune


def update_game_data(version):
    check_champions(version)
    check_runes(version)
    check_items(version)


def check_champions(version):  # Create/Update all champions.

    # Fetch all current Champion information from DDragon API.
    champions_info = ddragon_api(version=version, method='data', options='champion.json')

    # Loop through champions returned by API and Update/Create.
    for champion, value in champions_info['data'].items():
        obj, created = Champion.objects.update_or_create(
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

        print(f'New champion added: {obj.name}') if created else print(f'Champion updated: {obj.name}')


def check_runes(version):

    # Setup empty Rune.
    Rune.objects.get_or_create(
        rune_id=0,
        name='No Rune'
    )

    # Fetch all current Rune information from DDragon API.
    runes_info = ddragon_api(version=version, method='data', options='runesReforged.json')

    # Loop through runes returned by API and Update/Create.
    for tree in runes_info:
        for slot in tree['slots']:
            for rune in slot['runes']:
                obj, created = Rune.objects.update_or_create(
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

                print(f'New rune added: {obj.name}') if created else print(f'Rune updated: {obj.name}')


def check_items(version):

    # Setup empty Item.
    Item.objects.get_or_create(
        item_id=0,
        name='No Item'
    )

    # Fetch all current Item information from DDragon API.
    items_info = ddragon_api(version=version, method='data', options='item.json')

    # Loop through items returned by API and Update/Create.
    for item, value in items_info['data'].items():

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

        print(f'New item added: {obj.name}') if created else print(f'Item updated: {obj.name}')
