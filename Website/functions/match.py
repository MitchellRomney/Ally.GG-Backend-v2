import re

from django.db.models.signals import post_save

from Website.models import (Champion, Item, Match, Participant, Rune, Summoner,
                            SummonerSpell, Team)


def save_match(match_data, server):

    # Do not add matches that were before 2018 Pre-Season or that are tutorial games.
    if match_data['seasonId'] <= 10 or match_data['queueId'] > 2000:
        return False

    defaults = {}
    field_mappings = {
        'gameId': 'game_id',
        'platformId': 'platform_id',
        'queueId': 'queue_id',
        'seasonId': 'season_id',
        'mapId': 'map_id',
        'gameMode': 'game_mode',
        'gameType': 'game_type',
        'gameVersion': 'game_version',
        'gameDuration': 'game_duration',
        'timestamp': 'timestamp'
    }

    for field in match_data:
        if field in field_mappings:
            defaults[field_mappings[field]] = match_data[field]

    match_obj, created = Match.objects.update_or_create(
        game_id=match_data['gameId'],
        defaults=defaults
    )

    # Iterate through the teams, create according Team objects.
    blue_team = None
    red_team = None

    for team_data in match_data['teams']:
        if team_data['teamId'] == 100:
            blue_team = create_team(match_obj, team_data)
        else:
            red_team = create_team(match_obj, team_data)

    player_accounts = {}
    for participant_identity in match_data['participantIdentities']:
        player_accounts[participant_identity['participantId']] = participant_identity['player']

    participants = create_participants(match_obj, match_data, player_accounts, blue_team, red_team)
    Participant.objects.bulk_create(participants)

    return match_obj, [blue_team, red_team], participants


def create_team(match, team_data):

    team_obj, created = Team.objects.update_or_create(
        match=match,
        team_id=team_data['teamId'],
        defaults={
            'match': match,
            'win': False if team_data['win'] == 'Fail' or 'win' not in team_data else True,
            'team_id': team_data['teamId'],
            'first_dragon': team_data['firstDragon'],
            'first_inhibitor': team_data['firstInhibitor'],
            'first_rift_herald': team_data['firstRiftHerald'],
            'first_baron': team_data['firstBaron'],
            'baron_kills': team_data['baronKills'],
            'rift_herald_kills': team_data['riftHeraldKills'],
            'first_blood': team_data['firstBlood'],
            'first_tower': team_data['firstTower'],
            'inhibitor_kills': team_data['inhibitorKills'],
            'tower_kills': team_data['towerKills'],
            'dragon_kills': team_data['dragonKills'],
            'dominion_victory_score': team_data['dominionVictoryScore'],
            'vilemaw_kills': team_data['vilemawKills']
        }
    )

    return team_obj


def create_participants(match, match_data, player_accounts, blue_team, red_team):

    # Get the patch version from the game to fetch missing items & runes.
    patch = re.compile('\d\.\d{1,2}\.').findall(match.game_version)[0] + '1'

    new_participants = []

    for participant in match_data['participants']:
        player_account_info = player_accounts[participant['participantId']]

        if 'summonerId' in player_account_info:
            summoner, created = Summoner.objects.get_or_create(
                summoner_id=player_account_info['summonerId'],
                server=player_account_info['currentPlatformId'],
                defaults={
                    'summoner_name': player_account_info['summonerName'],
                    'summoner_id': player_account_info['summonerId'],
                    'account_id': player_account_info['currentAccountId'],
                    'server': player_account_info['currentPlatformId'],
                    'profile_icon_id': player_account_info['profileIcon'],
                    'summoner_level': 1
                }
            )
            if created:
                post_save.send(Summoner, instance=summoner, created=True)

        else:
            summoner = None

        if participant['timeline']['lane'] == 'BOTTOM':
            position = 'SUPPORT' if participant['timeline']['role'] == 'DUO_SUPPORT' else 'BOTTOM'
        else:
            position = participant['timeline']['lane']

        defaults = {
            'match': match,
            'platform_id': player_account_info['currentPlatformId'],
            'match_history_uri': player_account_info['matchHistoryUri'],
            'participant_id': participant['participantId'],
            'team': blue_team if participant['participantId'] <= 5 else red_team,
            'position': position,
            'champion': Champion.objects.get(key=participant['championId']),
            'summoner': summoner,
            'item0': Item.objects.get_or_create(
                item_id=participant['stats']['item0'],
                defaults={'item_id': participant['stats']['item0'], 'version': patch}
            )[0],
            'item1': Item.objects.get_or_create(
                item_id=participant['stats']['item1'],
                defaults={'item_id': participant['stats']['item1'], 'version': patch}
            )[0],
            'item2': Item.objects.get_or_create(
                item_id=participant['stats']['item2'],
                defaults={'item_id': participant['stats']['item2'], 'version': patch}
            )[0],
            'item3': Item.objects.get_or_create(
                item_id=participant['stats']['item3'],
                defaults={'item_id': participant['stats']['item3'], 'version': patch}
            )[0],
            'item4': Item.objects.get_or_create(
                item_id=participant['stats']['item4'],
                defaults={'item_id': participant['stats']['item4'], 'version': patch}
            )[0],
            'item5': Item.objects.get_or_create(
                item_id=participant['stats']['item5'],
                defaults={'item_id': participant['stats']['item5'], 'version': patch}
            )[0],
            'item6': Item.objects.get_or_create(
                item_id=participant['stats']['item6'],
                defaults={'item_id': participant['stats']['item6'], 'version': patch}
            )[0],
            'spell1_id': SummonerSpell.objects.get_or_create(
                key=participant['spell1Id'],
                defaults={'key': participant['spell1Id'], 'version': patch}
            )[0],
            'spell2_id': SummonerSpell.objects.get_or_create(
                key=participant['spell2Id'],
                defaults={'key': participant['spell2Id'], 'version': patch}
            )[0],
            'perk0': Rune.objects.get_or_create(
                rune_id=participant['stats']['perk0'],
                defaults={'rune_id': participant['stats']['perk0'], 'version': patch}
            )[0],
            'perk1': Rune.objects.get_or_create(
                rune_id=participant['stats']['perk1'],
                defaults={'rune_id': participant['stats']['perk1'], 'version': patch}
            )[0],
            'perk2': Rune.objects.get_or_create(
                rune_id=participant['stats']['perk2'],
                defaults={'rune_id': participant['stats']['perk2'], 'version': patch}
            )[0],
            'perk3': Rune.objects.get_or_create(
                rune_id=participant['stats']['perk3'],
                defaults={'rune_id': participant['stats']['perk3'], 'version': patch}
            )[0],
            'perk4': Rune.objects.get_or_create(
                rune_id=participant['stats']['perk4'],
                defaults={'rune_id': participant['stats']['perk4'], 'version': patch}
            )[0],
            'perk5': Rune.objects.get_or_create(
                rune_id=participant['stats']['perk5'],
                defaults={'rune_id': participant['stats']['perk5'], 'version': patch}
            )[0],
        }

        field_mappings = {
            'totalMinionsKilled': 'total_minions_killed',
            'neutralMinionsKilled': 'neutral_minions_killed',
            'neutralMinionsKilledTeamJungle': 'neutral_minions_killed_team_jungle',
            'neutralMinionsKilledEnemyJungle': 'neutral_minions_killed_enemy_jungle',
            'visionScore': 'vision_score',
            'sightWardsBoughtInGame': 'sight_wards_bought_in_game',
            'visionWardsBoughtInGame': 'vision_wards_bought_in_game',
            'wardsKilled': 'wards_killed',
            'wardsPlaced': 'wards_placed',
            'totalDamageDealt': 'total_damage_dealt',
            'totalDamageDealtToChampions': 'total_damage_dealt_to_champions',
            'physicalDamageDealt': 'physical_damage_dealt',
            'physicalDamageDealtToChampions': 'physical_damage_dealt_to_champions',
            'magicDamageDealt': 'magic_damage_dealt',
            'magicDamageDealtToChampions': 'magic_damage_dealt_to_champions',
            'trueDamageDealt': 'true_damage_dealt',
            'trueDamageDealtToChampions': 'true_damage_dealt_to_champions',
            'largestCriticalStrike': 'largest_critical_strike',
            'totalDamageTaken': 'total_damage_taken',
            'physicalDamageTaken': 'physical_damage_taken',
            'magicalDamageTaken': 'magical_damage_taken',
            'trueDamageTaken': 'true_damage_taken',
            'damageSelfMitigated': 'damage_self_mitigated',
            'turretKills': 'turret_kills',
            'inhibitorKills': 'inhibitor_kills',
            'damageDealtToTurrets': 'damage_dealt_to_turrets',
            'damageDealtToObjectives': 'damage_dealt_to_objectives',
            'firstInhibitorKill': 'first_inhibitor_kill',
            'firstInhibitorAssist': 'first_inhibitor_assist',
            'firstTowerAssist': 'first_tower_assist',
            'firstTowerKill': 'first_tower_kill',
            'kills': 'kills',
            'assists': 'assists',
            'killingSprees': 'killing_sprees',
            'unrealKills': 'unreal_kills',
            'doubleKills': 'double_kills',
            'tripleKills': 'triple_kills',
            'quadraKills': 'quadra_kills',
            'pentaKills': 'penta_kills',
            'largestMultiKill': 'largest_multi_kill',
            'largestKillingSpree': 'largest_killing_spree',
            'firstBloodKill': 'first_blood_kill',
            'firstBloodAssist': 'first_blood_assist',
            'timeCCingOthers': 'time_ccing_others',
            'totalTimeCrowdControlDealt': 'total_time_crowd_control_dealt',
            'totalUnitsHealed': 'total_units_healed',
            'totalHeal': 'total_heal',
            'deaths': 'deaths',
            'statPerk0': 'stat_perk0',
            'statPerk1': 'stat_perk1',
            'statPerk2': 'stat_perk2',
            'perk0Var1': 'perk0_var1',
            'perk0Var2': 'perk0_var2',
            'perk0Var3': 'perk0_var3',
            'perk1Var1': 'perk1_var1',
            'perk1Var2': 'perk1_var2',
            'perk1Var3': 'perk1_var3',
            'perk2Var1': 'perk2_var1',
            'perk2Var2': 'perk2_var2',
            'perk2Var3': 'perk2_var3',
            'perk3Var1': 'perk3_var1',
            'perk3Var2': 'perk3_var2',
            'perk3Var3': 'perk3_var3',
            'perk4Var1': 'perk4_var1',
            'perk4Var2': 'perk4_var2',
            'perk4Var3': 'perk4_var3',
            'perk5Var1': 'perk5_var1',
            'perk5Var2': 'perk5_var2',
            'perk5Var3': 'perk5_var3',
            'perkPrimaryStyle': 'perk_primary_style',
            'perkSubStyle': 'perk_sub_style',
            'playerScore0': 'player_score0',
            'playerScore1': 'player_score1',
            'playerScore2': 'player_score2',
            'playerScore3': 'player_score3',
            'playerScore4': 'player_score4',
            'playerScore5': 'player_score5',
            'playerScore6': 'player_score6',
            'playerScore7': 'player_score7',
            'playerScore8': 'player_score8',
            'playerScore9': 'player_score9',
            'objectivePlayerScore': 'objective_player_score',
            'combatPlayerScore': 'combat_player_score',
            'totalPlayerScore': 'total_player_score',
            'totalScoreRank': 'total_score_rank',
            'longestTimeSpentLiving': 'longest_time_spent_living',
            'goldEarned': 'gold_earned',
            'goldSpent': 'gold_spent',
            'win': 'win',
            'champLevel': 'champ_level'
        }

        for field in participant['stats']:
            if field in field_mappings:
                defaults[field_mappings[field]] = participant['stats'][field]

        participant = Participant()

        for field in defaults:
            setattr(participant, field, defaults[field])

        new_participants.append(participant)

    return new_participants
