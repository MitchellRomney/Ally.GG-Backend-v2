# Generated by Django 2.2.6 on 2019-10-26 04:40

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Champion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=255)),
                ('champ_id', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('key', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('blurb', models.TextField(max_length=255)),
                ('info_attack', models.BigIntegerField()),
                ('info_defense', models.BigIntegerField()),
                ('info_magic', models.BigIntegerField()),
                ('info_difficulty', models.BigIntegerField()),
                ('image_full', models.CharField(max_length=255)),
                ('image_sprite', models.CharField(max_length=255)),
                ('image_group', models.CharField(max_length=255)),
                ('image_x', models.BigIntegerField(default=0)),
                ('image_y', models.BigIntegerField(default=0)),
                ('image_w', models.BigIntegerField(default=0)),
                ('image_h', models.BigIntegerField(default=0)),
                ('tags', models.CharField(max_length=255)),
                ('partype', models.CharField(max_length=255)),
                ('stats_hp', models.DecimalField(decimal_places=4, max_digits=8)),
                ('stats_hpperlevel', models.DecimalField(decimal_places=4, max_digits=8)),
                ('stats_mp', models.DecimalField(decimal_places=4, max_digits=8)),
                ('stats_mpperlevel', models.DecimalField(decimal_places=4, max_digits=8)),
                ('stats_movespeed', models.DecimalField(decimal_places=4, max_digits=8)),
                ('stats_armor', models.DecimalField(decimal_places=4, max_digits=8)),
                ('stats_armorperlevel', models.DecimalField(decimal_places=4, max_digits=8)),
                ('stats_spellblock', models.DecimalField(decimal_places=4, max_digits=8)),
                ('stats_spellblockperlevel', models.DecimalField(decimal_places=4, max_digits=8)),
                ('stats_attackrange', models.DecimalField(decimal_places=4, max_digits=8)),
                ('stats_hpregen', models.DecimalField(decimal_places=4, max_digits=8)),
                ('stats_hpregenperlevel', models.DecimalField(decimal_places=4, max_digits=8)),
                ('stats_mpregen', models.DecimalField(decimal_places=4, max_digits=8)),
                ('stats_mpregenperlevel', models.DecimalField(decimal_places=4, max_digits=8)),
                ('stats_crit', models.DecimalField(decimal_places=4, max_digits=8)),
                ('stats_critperlevel', models.DecimalField(decimal_places=4, max_digits=8)),
                ('stats_attackdamage', models.DecimalField(decimal_places=4, max_digits=8)),
                ('stats_attackdamageperlevel', models.DecimalField(decimal_places=4, max_digits=8)),
                ('stats_attackspeedperlevel', models.DecimalField(decimal_places=4, max_digits=8)),
                ('stats_attackspeed', models.DecimalField(decimal_places=4, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('version', models.CharField(max_length=255)),
                ('item_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('colloq', models.CharField(blank=True, max_length=255, null=True)),
                ('plaintext', models.CharField(blank=True, max_length=255, null=True)),
                ('consumed', models.BooleanField(default=False)),
                ('stacks', models.IntegerField(default=1)),
                ('depth', models.IntegerField(default=1)),
                ('consume_on_full', models.BooleanField(default=False)),
                ('special_recipe', models.IntegerField(default=0)),
                ('in_store', models.BooleanField(default=True)),
                ('hide_from_all', models.BooleanField(default=False)),
                ('required_champion', models.CharField(max_length=255)),
                ('required_ally', models.CharField(max_length=255)),
                ('image_full', models.CharField(max_length=255)),
                ('image_sprite', models.CharField(max_length=255)),
                ('image_group', models.CharField(max_length=255)),
                ('image_x', models.IntegerField(default=0)),
                ('image_y', models.IntegerField(default=0)),
                ('image_w', models.IntegerField(default=0)),
                ('image_h', models.IntegerField(default=0)),
                ('gold_base', models.IntegerField(default=0)),
                ('gold_purchasable', models.BooleanField(default=True)),
                ('gold_total', models.IntegerField(default=0)),
                ('gold_sell', models.IntegerField(default=0)),
                ('tags', models.CharField(max_length=255)),
                ('maps_1', models.BooleanField(default=True)),
                ('maps_8', models.BooleanField(default=True)),
                ('maps_10', models.BooleanField(default=True)),
                ('maps_11', models.BooleanField(default=True)),
                ('maps_12', models.BooleanField(default=True)),
                ('FlatHPPoolMod', models.IntegerField(default=0)),
                ('rFlatHPModPerLevel', models.IntegerField(default=0)),
                ('FlatMPPoolMod', models.IntegerField(default=0)),
                ('rFlatMPModPerLevel', models.IntegerField(default=0)),
                ('PercentHPPoolMod', models.IntegerField(default=0)),
                ('PercentMPPoolMod', models.IntegerField(default=0)),
                ('FlatHPRegenMod', models.IntegerField(default=0)),
                ('rFlatHPRegenModPerLevel', models.IntegerField(default=0)),
                ('PercentHPRegenMod', models.IntegerField(default=0)),
                ('FlatMPRegenMod', models.IntegerField(default=0)),
                ('rFlatMPRegenModPerLevel', models.IntegerField(default=0)),
                ('PercentMPRegenMod', models.IntegerField(default=0)),
                ('FlatArmorMod', models.IntegerField(default=0)),
                ('rFlatArmorModPerLevel', models.IntegerField(default=0)),
                ('PercentArmorMod', models.IntegerField(default=0)),
                ('rFlatArmorPenetrationMod', models.IntegerField(default=0)),
                ('rFlatArmorPenetrationModPerLevel', models.IntegerField(default=0)),
                ('rPercentArmorPenetrationMod', models.IntegerField(default=0)),
                ('rPercentArmorPenetrationModPerLevel', models.IntegerField(default=0)),
                ('FlatPhysicalDamageMod', models.IntegerField(default=0)),
                ('rFlatPhysicalDamageModPerLevel', models.IntegerField(default=0)),
                ('PercentPhysicalDamageMod', models.IntegerField(default=0)),
                ('FlatMagicDamageMod', models.IntegerField(default=0)),
                ('rFlatMagicDamageModPerLevel', models.IntegerField(default=0)),
                ('PercentMagicDamageMod', models.IntegerField(default=0)),
                ('FlatMovementSpeedMod', models.IntegerField(default=0)),
                ('rFlatMovementSpeedModPerLevel', models.IntegerField(default=0)),
                ('PercentMovementSpeedMod', models.IntegerField(default=0)),
                ('rPercentMovementSpeedModPerLevel', models.IntegerField(default=0)),
                ('FlatAttackSpeedMod', models.IntegerField(default=0)),
                ('PercentAttackSpeedMod', models.IntegerField(default=0)),
                ('rPercentAttackSpeedModPerLevel', models.IntegerField(default=0)),
                ('rFlatDodgeMod', models.IntegerField(default=0)),
                ('rFlatDodgeModPerLevel', models.IntegerField(default=0)),
                ('PercentDodgeMod', models.IntegerField(default=0)),
                ('FlatCritChanceMod', models.IntegerField(default=0)),
                ('rFlatCritChanceModPerLevel', models.IntegerField(default=0)),
                ('PercentCritChanceMod', models.IntegerField(default=0)),
                ('FlatCritDamageMod', models.IntegerField(default=0)),
                ('rFlatCritDamageModPerLevel', models.IntegerField(default=0)),
                ('PercentCritDamageMod', models.IntegerField(default=0)),
                ('FlatBlockMod', models.IntegerField(default=0)),
                ('PercentBlockMod', models.IntegerField(default=0)),
                ('FlatSpellBlockMod', models.IntegerField(default=0)),
                ('rFlatSpellBlockModPerLevel', models.IntegerField(default=0)),
                ('PercentSpellBlockMod', models.IntegerField(default=0)),
                ('FlatEXPBonus', models.IntegerField(default=0)),
                ('PercentEXPBonus', models.IntegerField(default=0)),
                ('rPercentCooldownMod', models.IntegerField(default=0)),
                ('rPercentCooldownModPerLevel', models.IntegerField(default=0)),
                ('rFlatTimeDeadMod', models.IntegerField(default=0)),
                ('rFlatTimeDeadModPerLevel', models.IntegerField(default=0)),
                ('rPercentTimeDeadMod', models.IntegerField(default=0)),
                ('rPercentTimeDeadModPerLevel', models.IntegerField(default=0)),
                ('rFlatGoldPer10Mod', models.IntegerField(default=0)),
                ('rFlatMagicPenetrationMod', models.IntegerField(default=0)),
                ('rFlatMagicPenetrationModPerLevel', models.IntegerField(default=0)),
                ('rPercentMagicPenetrationMod', models.IntegerField(default=0)),
                ('rPercentMagicPenetrationModPerLevel', models.IntegerField(default=0)),
                ('FlatEnergyRegenMod', models.IntegerField(default=0)),
                ('rFlatEnergyRegenModPerLevel', models.IntegerField(default=0)),
                ('FlatEnergyPoolMod', models.IntegerField(default=0)),
                ('rFlatEnergyModPerLevel', models.IntegerField(default=0)),
                ('PercentLifeStealMod', models.IntegerField(default=0)),
                ('PercentSpellVampMod', models.IntegerField(default=0)),
                ('built_from', models.ManyToManyField(related_name='item_from', to='Website.Item')),
                ('built_into', models.ManyToManyField(related_name='item_into', to='Website.Item')),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platformId', models.CharField(max_length=255)),
                ('gameId', models.BigIntegerField(unique=True)),
                ('queueId', models.IntegerField(blank=True, choices=[(0, 'Custom'), (72, '1v1 Snowdown Showdown'), (73, '2v2 Snowdown Showdown'), (75, '6v6 Hexakill'), (76, 'Ultra Rapid Fire'), (78, 'One For All: Mirror Mode'), (83, 'Co-op vs AI Ultra Rapid Fire'), (98, '6v6 Hexakill'), (100, '5v5 ARAM'), (310, 'Nemesis'), (313, 'Black Market Brawlers'), (317, 'Definitely Not Dominion'), (325, 'All Random'), (400, '5v5 Draft Pick'), (420, '5v5 Ranked Solo'), (430, '5v5 Blind Pick'), (440, '5v5 Ranked Flex'), (450, '5v5 ARAM'), (460, '3v3 Blind Pick'), (470, '3v3 Ranked Flex'), (600, 'Blood Hunt Assassin'), (610, 'Dark Star: Singularity'), (700, 'Clash'), (800, 'Co-op vs. AI Intermediate Bot'), (810, 'Co-op vs. AI Intro Bot'), (820, 'Co-op vs. AI Beginner Bot'), (830, 'Co-op vs. AI Intro Bot'), (840, 'Co-op vs. AI Beginner Bot'), (850, 'Co-op vs. AI Intermediate Bot'), (900, 'ARURF'), (910, 'Ascension'), (920, 'Legend of the Poro King'), (940, 'Nexus Siege'), (950, 'Doom Bots Voting'), (960, 'Doom Bots Standard'), (980, 'Star Guardian Invasion: Normal'), (990, 'Star Guardian Invasion: Onslaught'), (1000, 'PROJECT: Hunters'), (1010, 'Snow ARURF'), (1020, 'One for All'), (1030, 'Odyssey Extraction: Intro'), (1040, 'Odyssey Extraction: Cadet'), (1050, 'Odyssey Extraction: Crewmember'), (1060, 'Odyssey Extraction: Captain'), (1070, 'Odyssey Extraction: Onslaught'), (1200, 'Nexus Blitz'), (2000, 'Tutorial 1'), (2010, 'Tutorial 2'), (2020, 'Tutorial 3')], null=True)),
                ('seasonId', models.IntegerField(blank=True, choices=[(0, 'PRESEASON 3'), (1, 'SEASON 3'), (2, 'PRESEASON 2014'), (3, 'SEASON 2014'), (4, 'PRESEASON 2015'), (5, 'SEASON 2015'), (6, 'PRESEASON 2016'), (7, 'SEASON 2016'), (8, 'PRESEASON 2017'), (9, 'SEASON 2017'), (10, 'PRESEASON 2018'), (11, 'SEASON 2018'), (12, 'PRESEASON 2019'), (13, 'SEASON 2019'), (14, 'PRESEASON 2020'), (15, 'SEASON 2020')], null=True)),
                ('mapId', models.IntegerField(blank=True, choices=[(1, "Summoner's Rift - Summer"), (2, "Summoner's Rift - Autumn"), (3, 'The Proving Grounds'), (4, 'Twisted Treeline - Original'), (8, 'The Crystal Scar'), (10, 'Twisted Treeline'), (11, "Summoner's Rift"), (12, 'Howling Abyss'), (14, "Butcher's Bridge"), (16, 'Cosmic Ruins'), (18, 'Valoran City Park'), (19, 'Substructure 43'), (20, 'Crash Site'), (21, 'Nexus Blitz')], null=True)),
                ('gameMode', models.CharField(max_length=255)),
                ('gameType', models.CharField(max_length=255)),
                ('gameVersion', models.CharField(max_length=255)),
                ('gameDuration', models.BigIntegerField()),
                ('timestamp', models.DateTimeField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Matches',
            },
        ),
        migrations.CreateModel(
            name='Rune',
            fields=[
                ('version', models.CharField(max_length=255)),
                ('rune_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('key', models.CharField(max_length=255)),
                ('icon', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('short_desc', models.TextField()),
                ('long_desc', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SummonerSpell',
            fields=[
                ('version', models.CharField(max_length=255, null=True)),
                ('key', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('summoner_spell_id', models.CharField(max_length=255, null=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('description', models.TextField(null=True)),
                ('tooltip', models.TextField(null=True)),
                ('maxrank', models.IntegerField(null=True)),
                ('cooldown', models.IntegerField(null=True)),
                ('cooldown_burn', models.CharField(max_length=255, null=True)),
                ('cost', models.IntegerField(null=True)),
                ('cost_burn', models.CharField(max_length=255, null=True)),
                ('cost_type', models.CharField(max_length=255, null=True)),
                ('summoner_level', models.IntegerField(null=True)),
                ('maxammo', models.CharField(max_length=255, null=True)),
                ('range', models.IntegerField(null=True)),
                ('range_burn', models.CharField(max_length=255, null=True)),
                ('image_full', models.CharField(max_length=255, null=True)),
                ('image_sprite', models.CharField(max_length=255, null=True)),
                ('image_group', models.CharField(max_length=255, null=True)),
                ('image_x', models.IntegerField(null=True)),
                ('image_y', models.IntegerField(null=True)),
                ('image_w', models.IntegerField(null=True)),
                ('image_h', models.IntegerField(null=True)),
                ('resource', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('win', models.BooleanField(default=False)),
                ('team_id', models.BigIntegerField()),
                ('first_dragon', models.BooleanField(default=False)),
                ('first_inhibitor', models.BooleanField(default=False)),
                ('first_rift_herald', models.BooleanField(default=False)),
                ('first_baron', models.BooleanField(default=False)),
                ('baron_kills', models.BigIntegerField()),
                ('rift_herald_kills', models.BigIntegerField()),
                ('first_blood', models.BooleanField(default=False)),
                ('first_tower', models.BooleanField(default=False)),
                ('inhibitor_kills', models.BigIntegerField()),
                ('tower_kills', models.BigIntegerField()),
                ('dragon_kills', models.BigIntegerField()),
                ('dominion_victory_score', models.BigIntegerField()),
                ('vilemaw_kills', models.BigIntegerField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('bans', models.ManyToManyField(related_name='Team_Bans', to='Website.Champion')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Teams', to='Website.Match')),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform_id', models.CharField(max_length=255)),
                ('match_history_uri', models.CharField(max_length=255)),
                ('participant_id', models.BigIntegerField()),
                ('positions', models.CharField(choices=[('TOP', 'Top'), ('JUNGLE', 'Jungle'), ('MIDDLE', 'Mid'), ('BOTTOM', 'ADC'), ('SUPPORT', 'Support'), ('NONE', 'None')], default='NONE', max_length=255)),
                ('neutral_minions_killed_team_jungle', models.BigIntegerField()),
                ('vision_score', models.BigIntegerField()),
                ('magic_damage_dealt_to_champions', models.BigIntegerField()),
                ('largest_multi_kill', models.BigIntegerField()),
                ('total_time_crowd_control_dealt', models.BigIntegerField()),
                ('longest_time_spent_living', models.BigIntegerField()),
                ('perk1_var1', models.BigIntegerField()),
                ('perk1_var3', models.BigIntegerField()),
                ('perk1_var2', models.BigIntegerField()),
                ('triple_kills', models.BigIntegerField()),
                ('player_score9', models.BigIntegerField()),
                ('player_score8', models.BigIntegerField()),
                ('kills', models.BigIntegerField()),
                ('player_score1', models.BigIntegerField()),
                ('player_score0', models.BigIntegerField()),
                ('player_score3', models.BigIntegerField()),
                ('player_score2', models.BigIntegerField()),
                ('player_score5', models.BigIntegerField()),
                ('player_score4', models.BigIntegerField()),
                ('player_score7', models.BigIntegerField()),
                ('player_score6', models.BigIntegerField()),
                ('perk5_var1', models.BigIntegerField()),
                ('perk5_var3', models.BigIntegerField()),
                ('perk5_var2', models.BigIntegerField()),
                ('total_score_rank', models.BigIntegerField()),
                ('neutral_minions_killed', models.BigIntegerField()),
                ('stat_perk1', models.BigIntegerField()),
                ('stat_perk0', models.BigIntegerField()),
                ('damage_dealt_to_turrets', models.BigIntegerField()),
                ('physical_damage_dealt_to_champions', models.BigIntegerField()),
                ('damage_dealt_to_objectives', models.BigIntegerField()),
                ('perk2_var2', models.BigIntegerField()),
                ('perk2_var3', models.BigIntegerField()),
                ('total_units_healed', models.BigIntegerField()),
                ('perk2_var1', models.BigIntegerField()),
                ('perk4_var1', models.BigIntegerField()),
                ('total_damage_taken', models.BigIntegerField()),
                ('perk4_var3', models.BigIntegerField()),
                ('wards_killed', models.BigIntegerField()),
                ('largest_critical_strike', models.BigIntegerField()),
                ('largest_killing_spree', models.BigIntegerField()),
                ('quadra_kills', models.BigIntegerField()),
                ('magic_damage_dealt', models.BigIntegerField()),
                ('first_blood_assist', models.BooleanField(default=False)),
                ('perk3_var3', models.BigIntegerField()),
                ('perk3_var2', models.BigIntegerField()),
                ('perk3_var1', models.BigIntegerField()),
                ('damage_self_mitigated', models.BigIntegerField()),
                ('magical_damage_taken', models.BigIntegerField()),
                ('perk0_var2', models.BigIntegerField()),
                ('first_inhibitor_kill', models.BooleanField(default=False)),
                ('true_damage_taken', models.BigIntegerField()),
                ('assists', models.BigIntegerField()),
                ('perk4_var2', models.BigIntegerField()),
                ('gold_spent', models.BigIntegerField()),
                ('true_damage_dealt', models.BigIntegerField()),
                ('physical_damage_dealt', models.BigIntegerField()),
                ('sight_wards_bought_in_game', models.BigIntegerField()),
                ('total_damage_dealt_to_champions', models.BigIntegerField()),
                ('physical_damage_taken', models.BigIntegerField()),
                ('total_player_score', models.BigIntegerField()),
                ('win', models.BooleanField(default=False)),
                ('objective_player_score', models.BigIntegerField()),
                ('total_damage_dealt', models.BigIntegerField()),
                ('neutral_minions_killed_enemy_jungle', models.BigIntegerField()),
                ('deaths', models.BigIntegerField()),
                ('wards_placed', models.BigIntegerField()),
                ('perk_primary_style', models.BigIntegerField()),
                ('perk_sub_style', models.BigIntegerField()),
                ('turret_kills', models.BigIntegerField()),
                ('first_blood_kill', models.BooleanField(default=False)),
                ('true_damage_dealt_to_champions', models.BigIntegerField()),
                ('gold_earned', models.BigIntegerField()),
                ('killing_sprees', models.BigIntegerField()),
                ('unreal_kills', models.BigIntegerField()),
                ('first_tower_assist', models.BooleanField(default=False)),
                ('first_tower_kill', models.BooleanField(default=False)),
                ('champ_level', models.BigIntegerField()),
                ('double_kills', models.BigIntegerField()),
                ('inhibitor_kills', models.BigIntegerField()),
                ('first_inhibitor_assist', models.BooleanField(default=False)),
                ('perk0_var1', models.BigIntegerField()),
                ('combat_player_score', models.BigIntegerField()),
                ('perk0_var3', models.BigIntegerField()),
                ('vision_wards_bought_in_game', models.BigIntegerField()),
                ('penta_kills', models.BigIntegerField()),
                ('total_heal', models.BigIntegerField()),
                ('total_minions_killed', models.BigIntegerField()),
                ('time_ccing_others', models.BigIntegerField()),
                ('stat_perk2', models.BigIntegerField()),
                ('cs10_deltas', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), null=True, size=None)),
                ('skill_order', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1), null=True, size=None)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('champion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Players', to='Website.Champion')),
                ('item0', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Player_Items_1', to='Website.Item')),
                ('item1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Player_Items_2', to='Website.Item')),
                ('item2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Player_Items_3', to='Website.Item')),
                ('item3', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Player_Items_4', to='Website.Item')),
                ('item4', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Player_Items_5', to='Website.Item')),
                ('item5', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Player_Items_6', to='Website.Item')),
                ('item6', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Player_Items_7', to='Website.Item')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Players', to='Website.Match')),
                ('perk0', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Player_Runes_1', to='Website.Rune')),
                ('perk1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Player_Runes_2', to='Website.Rune')),
                ('perk2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Player_Runes_3', to='Website.Rune')),
                ('perk3', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Player_Runes_4', to='Website.Rune')),
                ('perk4', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Player_Runes_5', to='Website.Rune')),
                ('perk5', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Player_Runes_6', to='Website.Rune')),
                ('spell1_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Player_Spells_1', to='Website.SummonerSpell')),
                ('spell2_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Player_Spells_2', to='Website.SummonerSpell')),
                ('summoner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Players', to='Website.Summoner')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Website.Team')),
            ],
        ),
    ]
