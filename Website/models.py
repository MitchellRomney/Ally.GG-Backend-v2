import json

from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Notification(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    user = models.ForeignKey(User, related_name='Notification_Users', on_delete=models.SET_NULL, blank=True, null=True)
    CATEGORIES = (
        ('ALERT', 'Alert'),
        ('NEWS', 'News'),
        ('DEBUG', 'Debug'),
    )
    category = models.CharField(max_length=255, choices=CATEGORIES)
    seen = models.BooleanField(default=False)

    date_created = models.DateTimeField(auto_now_add=True, blank=False)
    date_modified = models.DateTimeField(auto_now=True, blank=False)


class RankedTier(models.Model):
    key = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)
    order = models.IntegerField()

    def __str__(self):
        return self.name


class AccessCode(models.Model):
    key = models.CharField(max_length=32, blank=False, null=False)

    user = models.ForeignKey(User, related_name="Access_Codes", on_delete=models.SET_NULL, blank=True, null=True)
    used = models.BooleanField(default=False)
    date_used = models.DateTimeField(blank=True, null=True)

    archived = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, blank=False)

    def __str__(self):
        return self.key


class RegistrationInterest(models.Model):
    first_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='RegistrationInterest_User', on_delete=models.SET_NULL, blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True, blank=False)
    date_modified = models.DateTimeField(auto_now=True, blank=False)

    def __str__(self):
        return self.email


class SummonerSpell(models.Model):
    version = models.CharField(max_length=255, null=True)
    key = models.IntegerField(blank=False, unique=True, primary_key=True)
    summoner_spell_id = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    tooltip = models.TextField(null=True)
    maxrank = models.IntegerField(null=True)
    cooldown = models.IntegerField(null=True)
    cooldown_burn = models.CharField(max_length=255, null=True)
    cost = models.IntegerField(null=True)
    cost_burn = models.CharField(max_length=255, null=True)
    cost_type = models.CharField(max_length=255, null=True)
    summoner_level = models.IntegerField(null=True)
    maxammo = models.CharField(max_length=255, null=True)
    range = models.IntegerField(null=True)
    range_burn = models.CharField(max_length=255, null=True)
    image_full = models.CharField(max_length=255, null=True)
    image_sprite = models.CharField(max_length=255, null=True)
    image_group = models.CharField(max_length=255, null=True)
    image_x = models.IntegerField(null=True)
    image_y = models.IntegerField(null=True)
    image_w = models.IntegerField(null=True)
    image_h = models.IntegerField(null=True)
    resource = models.CharField(max_length=255, null=True)

    def __str__(self):
        return str(self.name)


class Rune(models.Model):
    version = models.CharField(max_length=255, blank=False)
    rune_id = models.IntegerField(blank=False, unique=True, primary_key=True)
    key = models.CharField(max_length=255, blank=False)
    icon = models.CharField(max_length=255, blank=False)
    name = models.CharField(max_length=255, blank=False)
    short_desc = models.TextField(blank=False)
    long_desc = models.TextField(blank=False)

    def __str__(self):
        return str(self.name)


class Item(models.Model):
    version = models.CharField(max_length=255)
    item_id = models.IntegerField(blank=False, unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=False)
    colloq = models.CharField(max_length=255, null=True, blank=True)
    plaintext = models.CharField(max_length=255, null=True, blank=True)
    built_into = models.ManyToManyField('Item', related_name='item_into')
    built_from = models.ManyToManyField('Item', related_name='item_from')
    consumed = models.BooleanField(default=False)
    stacks = models.IntegerField(default=1)
    depth = models.IntegerField(default=1)
    consume_on_full = models.BooleanField(default=False)
    special_recipe = models.IntegerField(default=0)
    in_store = models.BooleanField(default=True)
    hide_from_all = models.BooleanField(default=False)
    required_champion = models.CharField(max_length=255)
    required_ally = models.CharField(max_length=255)

    image_full = models.CharField(max_length=255)
    image_sprite = models.CharField(max_length=255)
    image_group = models.CharField(max_length=255)
    image_x = models.IntegerField(default=0)
    image_y = models.IntegerField(default=0)
    image_w = models.IntegerField(default=0)
    image_h = models.IntegerField(default=0)

    gold_base = models.IntegerField(default=0)
    gold_purchasable = models.BooleanField(default=True)
    gold_total = models.IntegerField(default=0)
    gold_sell = models.IntegerField(default=0)

    tags = models.CharField(max_length=255)

    maps_1 = models.BooleanField(default=True)
    maps_8 = models.BooleanField(default=True)
    maps_10 = models.BooleanField(default=True)
    maps_11 = models.BooleanField(default=True)
    maps_12 = models.BooleanField(default=True)

    flat_hp_pool_mod = models.IntegerField(default=0)
    r_flat_hp_mod_per_level = models.IntegerField(default=0)
    flat_mp_pool_mod = models.IntegerField(default=0)
    r_flat_mp_mod_per_level = models.IntegerField(default=0)
    percent_hp_pool_mod = models.IntegerField(default=0)
    percent_mp_pool_mod = models.IntegerField(default=0)
    flat_hp_regen_mod = models.IntegerField(default=0)
    r_flat_hp_regen_mod_per_level = models.IntegerField(default=0)
    percent_hp_regen_mod = models.IntegerField(default=0)
    flat_mp_regen_mod = models.IntegerField(default=0)
    r_flat_mp_regen_mod_per_level = models.IntegerField(default=0)
    percent_mp_regen_mod = models.IntegerField(default=0)
    flat_armor_mod = models.IntegerField(default=0)
    r_flat_armor_mod_per_level = models.IntegerField(default=0)
    percent_armor_mod = models.IntegerField(default=0)
    r_flat_armor_penetration_mod = models.IntegerField(default=0)
    r_flat_armor_penetration_mod_per_level = models.IntegerField(default=0)
    r_percent_armor_penetration_mod = models.IntegerField(default=0)
    r_percent_armor_penetration_mod_per_level = models.IntegerField(default=0)
    flat_physical_damage_mod = models.IntegerField(default=0)
    r_flat_physical_damage_mod_per_level = models.IntegerField(default=0)
    percent_physical_damage_mod = models.IntegerField(default=0)
    flat_magic_damage_mod = models.IntegerField(default=0)
    r_flat_magic_damage_mod_per_level = models.IntegerField(default=0)
    percent_magic_damage_mod = models.IntegerField(default=0)
    flat_movement_speed_mod = models.IntegerField(default=0)
    r_flat_movement_speed_mod_per_level = models.IntegerField(default=0)
    percent_movement_speed_mod = models.IntegerField(default=0)
    r_percent_movement_speed_mod_per_level = models.IntegerField(default=0)
    flat_attack_speed_mod = models.IntegerField(default=0)
    percent_attack_speed_mod = models.IntegerField(default=0)
    r_percent_attack_speed_mod_per_level = models.IntegerField(default=0)
    r_flat_dodge_mod = models.IntegerField(default=0)
    r_flat_dodge_mod_per_level = models.IntegerField(default=0)
    percent_dodge_mod = models.IntegerField(default=0)
    flat_crit_chance_mod = models.IntegerField(default=0)
    r_flat_crit_chance_mod_per_level = models.IntegerField(default=0)
    percent_crit_chance_mod = models.IntegerField(default=0)
    flat_crit_damage_mod = models.IntegerField(default=0)
    r_flat_crit_damage_mod_per_level = models.IntegerField(default=0)
    percent_crit_damage_mod = models.IntegerField(default=0)
    flat_block_mod = models.IntegerField(default=0)
    percent_block_mod = models.IntegerField(default=0)
    flat_spell_block_mod = models.IntegerField(default=0)
    r_flat_spell_block_mod_per_level = models.IntegerField(default=0)
    percent_spell_block_mod = models.IntegerField(default=0)
    flat_exp_bonus = models.IntegerField(default=0)
    percent_exp_bonus = models.IntegerField(default=0)
    r_percent_cooldown_mod = models.IntegerField(default=0)
    r_percent_cooldown_mod_per_level = models.IntegerField(default=0)
    r_flat_time_dead_mod = models.IntegerField(default=0)
    r_flat_time_dead_mod_per_level = models.IntegerField(default=0)
    r_percent_time_dead_mod = models.IntegerField(default=0)
    r_percent_time_dead_mod_per_level = models.IntegerField(default=0)
    r_flat_gold_per10_mod = models.IntegerField(default=0)
    r_flat_magic_penetration_mod = models.IntegerField(default=0)
    r_flat_magic_penetration_mod_per_level = models.IntegerField(default=0)
    r_percent_magic_penetration_mod = models.IntegerField(default=0)
    r_percent_magic_penetration_mod_per_level = models.IntegerField(default=0)
    flat_energy_regen_mod = models.IntegerField(default=0)
    r_flat_energy_regen_mod_per_level = models.IntegerField(default=0)
    flat_energy_pool_mod = models.IntegerField(default=0)
    r_flat_energy_mod_per_level = models.IntegerField(default=0)
    percent_life_steal_mod = models.IntegerField(default=0)
    percent_spell_vamp_mod = models.IntegerField(default=0)

    def set_tags(self, x):
        self.tags = json.dumps(x)

    def get_tags(self):
        return json.loads(self.tags)

    def __str__(self):
        return str(self.name)


class Champion(models.Model):
    # General
    version = models.CharField(max_length=255, blank=False)  # Champion updated version (should be latest).
    champ_id = models.CharField(max_length=255, blank=False)  # Basically champion name without spaces and extras.
    name = models.CharField(max_length=255, blank=False)
    key = models.CharField(max_length=255, blank=False)  # Numerical ID
    title = models.CharField(max_length=255, blank=False)
    blurb = models.TextField(max_length=255, blank=False)
    info_attack = models.BigIntegerField(blank=False)
    info_defense = models.BigIntegerField(blank=False)
    info_magic = models.BigIntegerField(blank=False)
    info_difficulty = models.BigIntegerField(blank=False)

    # Images
    image_full = models.CharField(max_length=255, blank=False)
    image_sprite = models.CharField(max_length=255, blank=False)
    image_group = models.CharField(max_length=255, blank=False)
    image_x = models.BigIntegerField(blank=False, default=0)
    image_y = models.BigIntegerField(blank=False, default=0)
    image_w = models.BigIntegerField(blank=False, default=0)
    image_h = models.BigIntegerField(blank=False, default=0)

    # Stats & Info
    tags = models.CharField(max_length=255, blank=False)
    partype = models.CharField(max_length=255, blank=False)
    stats_hp = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_hpperlevel = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_mp = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_mpperlevel = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_movespeed = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_armor = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_armorperlevel = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_spellblock = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_spellblockperlevel = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_attackrange = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_hpregen = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_hpregenperlevel = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_mpregen = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_mpregenperlevel = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_crit = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_critperlevel = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_attackdamage = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_attackdamageperlevel = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_attackspeedperlevel = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_attackspeed = models.DecimalField(max_digits=8, decimal_places=4, blank=False)

    def set_tags(self, x):
        self.tags = json.dumps(x)

    def get_tags(self):
        return json.loads(self.tags)

    def __str__(self):
        return self.champ_id


class Profile(models.Model):
    user = models.ForeignKey(User, related_name="Profiles", on_delete=models.CASCADE, blank=False)
    main_summoner = models.ForeignKey('Summoner', related_name='Main_Summoners', on_delete=models.SET_NULL, null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)
    third_party_token = models.CharField(max_length=12, blank=True, null=True)

    archived = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, blank=False)
    date_modified = models.DateTimeField(auto_now=True, blank=False)

    def __str__(self):
        return self.user.username


class Summoner(models.Model):
    summoner_name = models.CharField(max_length=255, blank=False)
    summoner_id = models.CharField(max_length=255, blank=False)
    puuid = models.CharField(max_length=255, blank=True)
    account_id = models.CharField(max_length=255, blank=True)
    user_profile = models.ForeignKey(
        Profile,
        related_name="summoners",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # General
    SERVERS = (
        ('BR1', 'Brazil'),
        ('EUN1', 'EU Nordic & East'),
        ('EUW1', 'EU West'),
        ('JP1', 'Japan'),
        ('KR', 'Korea'),
        ('LA1', 'Latin America North'),
        ('LA2', 'Latin America South'),
        ('NA1', 'North America'),
        ('OC1', 'Oceania'),
        ('TR1', 'Turkey'),
        ('RU', 'Russia'),
        ('PBE1', 'Public Beta Environment'),
    )
    server = models.CharField(max_length=255, choices=SERVERS)
    profile_icon_id = models.BigIntegerField(default=0)
    summoner_level = models.IntegerField(blank=True)

    # SoloQ
    ranked_solo_league_id = models.CharField(max_length=255, blank=True)
    ranked_solo_league_name = models.CharField(max_length=255, blank=True)
    ranked_solo_hot_streak = models.BooleanField(default=False)
    ranked_solo_wins = models.BigIntegerField(default=0)
    ranked_solo_losses = models.BigIntegerField(default=0)
    ranked_solo_veteran = models.BooleanField(default=False)
    ranked_solo_rank = models.CharField(max_length=255, blank=True)
    ranked_solo_inactive = models.BooleanField(default=False)
    ranked_solo_fresh_blood = models.BooleanField(default=False)
    ranked_solo_league_points = models.BigIntegerField(default=0)
    ranked_solo_tier = models.ForeignKey(
        RankedTier,
        related_name="ranked_solo_tiers",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Flex SR
    ranked_flex_sr_league_id = models.CharField(max_length=255, blank=True)
    ranked_flex_sr_league_name = models.CharField(max_length=255, blank=True)
    ranked_flex_sr_hot_streak = models.BooleanField(default=False)
    ranked_flex_sr_wins = models.BigIntegerField(default=0)
    ranked_flex_sr_losses = models.BigIntegerField(default=0)
    ranked_flex_sr_veteran = models.BooleanField(default=False)
    ranked_flex_sr_rank = models.CharField(max_length=255, blank=True)
    ranked_flex_sr_inactive = models.BooleanField(default=False)
    ranked_flex_sr_fresh_blood = models.BooleanField(default=False)
    ranked_flex_sr_league_points = models.BigIntegerField(default=0)
    ranked_flex_sr_tier = models.ForeignKey(
        RankedTier,
        related_name="ranked_flex_sr_tiers",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Flex TT
    ranked_flex_tt_league_id = models.CharField(max_length=255, blank=True)
    ranked_flex_tt_league_name = models.CharField(max_length=255, blank=True)
    ranked_flex_tt_hot_streak = models.BooleanField(default=False)
    ranked_flex_tt_wins = models.BigIntegerField(default=0)
    ranked_flex_tt_losses = models.BigIntegerField(default=0)
    ranked_flex_tt_veteran = models.BooleanField(default=False)
    ranked_flex_tt_rank = models.CharField(max_length=255, blank=True)
    ranked_flex_tt_inactive = models.BooleanField(default=False)
    ranked_flex_tt_fresh_blood = models.BooleanField(default=False)
    ranked_flex_tt_league_points = models.BigIntegerField(default=0)
    ranked_flex_tt_tier = models.ForeignKey(
        RankedTier,
        related_name="ranked_flex_tt_tiers",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # System
    date_created = models.DateTimeField(auto_now_add=True, blank=False)
    date_updated = models.DateTimeField(null=True)

    def __str__(self):
        return self.summoner_name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['summoner_id', 'server'], name='Unique Summoner Id by Server'),
            models.UniqueConstraint(fields=['account_id', 'server'], name='Unique Account Id by Server')
        ]


class Match(models.Model):
    # IDs
    platform_id = models.CharField(max_length=255)
    game_id = models.BigIntegerField(unique=True)
    QUEUES = (
        (0, 'Custom'),
        (72, '1v1 Snowdown Showdown'),
        (73, '2v2 Snowdown Showdown'),
        (75, '6v6 Hexakill'),
        (76, 'Ultra Rapid Fire'),
        (78, 'One For All: Mirror Mode'),
        (83, 'Co-op vs AI Ultra Rapid Fire'),
        (98, '6v6 Hexakill'),
        (100, '5v5 ARAM'),
        (310, 'Nemesis'),
        (313, 'Black Market Brawlers'),
        (317, 'Definitely Not Dominion'),
        (325, 'All Random'),
        (400, '5v5 Draft Pick'),
        (420, '5v5 Ranked Solo'),
        (430, '5v5 Blind Pick'),
        (440, '5v5 Ranked Flex'),
        (450, '5v5 ARAM'),
        (460, '3v3 Blind Pick'),
        (470, '3v3 Ranked Flex'),
        (600, 'Blood Hunt Assassin'),
        (610, 'Dark Star: Singularity'),
        (700, 'Clash'),
        (800, 'Co-op vs. AI Intermediate Bot'),
        (810, 'Co-op vs. AI Intro Bot'),
        (820, 'Co-op vs. AI Beginner Bot'),
        (830, 'Co-op vs. AI Intro Bot'),
        (840, 'Co-op vs. AI Beginner Bot'),
        (850, 'Co-op vs. AI Intermediate Bot'),
        (900, 'URF'),
        (910, 'Ascension'),
        (920, 'Legend of the Poro King'),
        (940, 'Nexus Siege'),
        (950, 'Doom Bots Voting'),
        (960, 'Doom Bots Standard'),
        (980, 'Star Guardian Invasion: Normal'),
        (990, 'Star Guardian Invasion: Onslaught'),
        (1000, 'PROJECT: Hunters'),
        (1010, 'Snow ARURF'),
        (1020, 'One for All'),
        (1030, 'Odyssey Extraction: Intro'),
        (1040, 'Odyssey Extraction: Cadet'),
        (1050, 'Odyssey Extraction: Crewmember'),
        (1060, 'Odyssey Extraction: Captain'),
        (1070, 'Odyssey Extraction: Onslaught'),
        (1200, 'Nexus Blitz'),
        (2000, 'Tutorial 1'),
        (2010, 'Tutorial 2'),
        (2020, 'Tutorial 3'),
    )
    queue_id = models.IntegerField(choices=QUEUES, null=True, blank=True)
    SEASONS = (
        (0, 'PRESEASON 3'),
        (1, 'SEASON 3'),
        (2, 'PRESEASON 2014'),
        (3, 'SEASON 2014'),
        (4, 'PRESEASON 2015'),
        (5, 'SEASON 2015'),
        (6, 'PRESEASON 2016'),
        (7, 'SEASON 2016'),
        (8, 'PRESEASON 2017'),
        (9, 'SEASON 2017'),
        (10, 'PRESEASON 2018'),
        (11, 'SEASON 2018'),
        (12, 'PRESEASON 2019'),
        (13, 'SEASON 2019'),
        (14, 'PRESEASON 2020'),
        (15, 'SEASON 2020')
    )
    season_id = models.IntegerField(choices=SEASONS, null=True, blank=True)
    MAPS = (
        (1, 'Summoner\'s Rift - Summer'),
        (2, 'Summoner\'s Rift - Autumn'),
        (3, 'The Proving Grounds'),
        (4, 'Twisted Treeline - Original'),
        (8, 'The Crystal Scar'),
        (10, 'Twisted Treeline'),
        (11, 'Summoner\'s Rift'),
        (12, 'Howling Abyss'),
        (14, 'Butcher\'s Bridge'),
        (16, 'Cosmic Ruins'),
        (18, 'Valoran City Park'),
        (19, 'Substructure 43'),
        (20, 'Crash Site'),
        (21, 'Nexus Blitz'),
    )
    map_id = models.IntegerField(choices=MAPS, null=True, blank=True)

    # Match Information
    game_mode = models.CharField(max_length=255)
    game_type = models.CharField(max_length=255)
    game_version = models.CharField(max_length=255)
    game_duration = models.BigIntegerField()
    timestamp = models.DateTimeField()

    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.game_id)

    class Meta:
        verbose_name_plural = "Matches"


class Team(models.Model):
    # IDs
    match = models.ForeignKey(Match, related_name='Teams', on_delete=models.CASCADE)

    # General
    win = models.BooleanField(default=False)  # 'Fail' = False, 'Win' = True
    team_id = models.BigIntegerField(blank=False)  # 100 = Team1, 200 = Team2
    bans = models.ManyToManyField(Champion, related_name='Team_Bans')

    # Summoners Rift
    first_dragon = models.BooleanField(default=False)
    first_inhibitor = models.BooleanField(default=False)
    first_rift_herald = models.BooleanField(default=False)
    first_baron = models.BooleanField(default=False)
    baron_kills = models.BigIntegerField(blank=False)
    rift_herald_kills = models.BigIntegerField(blank=False)
    first_blood = models.BooleanField(default=False)
    first_tower = models.BooleanField(default=False)
    inhibitor_kills = models.BigIntegerField(blank=False)
    tower_kills = models.BigIntegerField(blank=False)
    dragon_kills = models.BigIntegerField(blank=False)

    # Other
    dominion_victory_score = models.BigIntegerField(blank=False)
    vilemaw_kills = models.BigIntegerField(blank=False)

    # System
    date_created = models.DateTimeField(auto_now_add=True, blank=False)
    date_modified = models.DateTimeField(auto_now=True, blank=False)

    def __str__(self):
        team = 'Blue' if self.team_id == 100 else 'Red'
        return str(self.match) + ' - Team: ' + team


class Participant(models.Model):
    match = models.ForeignKey(Match, related_name='Players', on_delete=models.CASCADE, blank=False)
    summoner = models.ForeignKey(Summoner, related_name='Players', on_delete=models.SET_NULL, blank=True, null=True)
    platform_id = models.CharField(max_length=255, blank=False)
    match_history_uri = models.CharField(max_length=255, blank=False)
    participant_id = models.BigIntegerField(blank=False)

    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    POSITIONS = (
        ('TOP', 'Top'),
        ('JUNGLE', 'Jungle'),
        ('MIDDLE', 'Mid'),
        ('BOTTOM', 'ADC'),
        ('SUPPORT', 'Support'),
        ('NONE', 'None')
    )
    position = models.CharField(max_length=255, choices=POSITIONS, null=False, blank=False, default='NONE')

    # Participant Stats
    champion = models.ForeignKey(Champion, related_name='Players', on_delete=models.SET_NULL, blank=False, null=True)
    spell1_id = models.ForeignKey(SummonerSpell, related_name='Player_Spells_1', on_delete=models.SET_NULL, null=True)
    spell2_id = models.ForeignKey(SummonerSpell, related_name='Player_Spells_2', on_delete=models.SET_NULL, null=True)
    neutral_minions_killed_team_jungle = models.BigIntegerField(default=0)
    vision_score = models.BigIntegerField(default=0)
    magic_damage_dealt_to_champions = models.BigIntegerField(default=0)
    largest_multi_kill = models.BigIntegerField(default=0)
    total_time_crowd_control_dealt = models.BigIntegerField(default=0)
    longest_time_spent_living = models.BigIntegerField(default=0)
    perk1_var1 = models.BigIntegerField(default=0)
    perk1_var3 = models.BigIntegerField(default=0)
    perk1_var2 = models.BigIntegerField(default=0)
    triple_kills = models.BigIntegerField(default=0)
    perk5 = models.ForeignKey(Rune, related_name='Player_Runes_6', on_delete=models.SET_NULL, blank=False, null=True)
    perk4 = models.ForeignKey(Rune, related_name='Player_Runes_5', on_delete=models.SET_NULL, blank=False, null=True)
    player_score9 = models.BigIntegerField(default=0)
    player_score8 = models.BigIntegerField(default=0)
    kills = models.BigIntegerField(default=0)
    player_score1 = models.BigIntegerField(default=0)
    player_score0 = models.BigIntegerField(default=0)
    player_score3 = models.BigIntegerField(default=0)
    player_score2 = models.BigIntegerField(default=0)
    player_score5 = models.BigIntegerField(default=0)
    player_score4 = models.BigIntegerField(default=0)
    player_score7 = models.BigIntegerField(default=0)
    player_score6 = models.BigIntegerField(default=0)
    perk5_var1 = models.BigIntegerField(default=0)
    perk5_var3 = models.BigIntegerField(default=0)
    perk5_var2 = models.BigIntegerField(default=0)
    total_score_rank = models.BigIntegerField(default=0)
    neutral_minions_killed = models.BigIntegerField(default=0)
    stat_perk1 = models.BigIntegerField(default=0)
    stat_perk0 = models.BigIntegerField(default=0)
    damage_dealt_to_turrets = models.BigIntegerField(default=0)
    physical_damage_dealt_to_champions = models.BigIntegerField(default=0)
    damage_dealt_to_objectives = models.BigIntegerField(default=0)
    perk2_var2 = models.BigIntegerField(default=0)
    perk2_var3 = models.BigIntegerField(default=0)
    total_units_healed = models.BigIntegerField(default=0)
    perk2_var1 = models.BigIntegerField(default=0)
    perk4_var1 = models.BigIntegerField(default=0)
    total_damage_taken = models.BigIntegerField(default=0)
    perk4_var3 = models.BigIntegerField(default=0)
    wards_killed = models.BigIntegerField(default=0)
    largest_critical_strike = models.BigIntegerField(default=0)
    largest_killing_spree = models.BigIntegerField(default=0)
    quadra_kills = models.BigIntegerField(default=0)
    magic_damage_dealt = models.BigIntegerField(default=0)
    first_blood_assist = models.BooleanField(default=False)
    item2 = models.ForeignKey(Item, related_name='Player_Items_3', on_delete=models.SET_NULL, null=True)
    item3 = models.ForeignKey(Item, related_name='Player_Items_4', on_delete=models.SET_NULL, null=True)
    item0 = models.ForeignKey(Item, related_name='Player_Items_1', on_delete=models.SET_NULL, null=True)
    item1 = models.ForeignKey(Item, related_name='Player_Items_2', on_delete=models.SET_NULL, null=True)
    item6 = models.ForeignKey(Item, related_name='Player_Items_7', on_delete=models.SET_NULL, null=True)
    item4 = models.ForeignKey(Item, related_name='Player_Items_5', on_delete=models.SET_NULL, null=True)
    item5 = models.ForeignKey(Item, related_name='Player_Items_6', on_delete=models.SET_NULL, null=True)
    perk1 = models.ForeignKey(Rune, related_name='Player_Runes_2', on_delete=models.SET_NULL, blank=False, null=True)
    perk0 = models.ForeignKey(Rune, related_name='Player_Runes_1', on_delete=models.SET_NULL, blank=False, null=True)
    perk3 = models.ForeignKey(Rune, related_name='Player_Runes_4', on_delete=models.SET_NULL, blank=False, null=True)
    perk2 = models.ForeignKey(Rune, related_name='Player_Runes_3', on_delete=models.SET_NULL, blank=False, null=True)
    perk3_var3 = models.BigIntegerField(default=0)
    perk3_var2 = models.BigIntegerField(default=0)
    perk3_var1 = models.BigIntegerField(default=0)
    damage_self_mitigated = models.BigIntegerField(default=0)
    magical_damage_taken = models.BigIntegerField(default=0)
    perk0_var2 = models.BigIntegerField(default=0)
    first_inhibitor_kill = models.BooleanField(default=False)
    true_damage_taken = models.BigIntegerField(default=0)
    assists = models.BigIntegerField(default=0)
    perk4_var2 = models.BigIntegerField(default=0)
    gold_spent = models.BigIntegerField(default=0)
    true_damage_dealt = models.BigIntegerField(default=0)
    physical_damage_dealt = models.BigIntegerField(default=0)
    sight_wards_bought_in_game = models.BigIntegerField(default=0)
    total_damage_dealt_to_champions = models.BigIntegerField(default=0)
    physical_damage_taken = models.BigIntegerField(default=0)
    total_player_score = models.BigIntegerField(default=0)
    win = models.BooleanField(default=False)
    objective_player_score = models.BigIntegerField(default=0)
    total_damage_dealt = models.BigIntegerField(default=0)
    neutral_minions_killed_enemy_jungle = models.BigIntegerField(default=0)
    deaths = models.BigIntegerField(default=0)
    wards_placed = models.BigIntegerField(default=0)
    perk_primary_style = models.BigIntegerField(default=0)
    perk_sub_style = models.BigIntegerField(default=0)
    turret_kills = models.BigIntegerField(default=0)
    first_blood_kill = models.BooleanField(default=False)
    true_damage_dealt_to_champions = models.BigIntegerField(default=0)
    gold_earned = models.BigIntegerField(default=0)
    killing_sprees = models.BigIntegerField(default=0)
    unreal_kills = models.BigIntegerField(default=0)
    first_tower_assist = models.BooleanField(default=False)
    first_tower_kill = models.BooleanField(default=False)
    champ_level = models.BigIntegerField(default=0)
    double_kills = models.BigIntegerField(default=0)
    inhibitor_kills = models.BigIntegerField(default=0)
    first_inhibitor_assist = models.BooleanField(default=False)
    perk0_var1 = models.BigIntegerField(default=0)
    combat_player_score = models.BigIntegerField(default=0)
    perk0_var3 = models.BigIntegerField(default=0)
    vision_wards_bought_in_game = models.BigIntegerField(default=0)
    penta_kills = models.BigIntegerField(default=0)
    total_heal = models.BigIntegerField(default=0)
    total_minions_killed = models.BigIntegerField(default=0)
    time_ccing_others = models.BigIntegerField(default=0)
    stat_perk2 = models.BigIntegerField(default=0)
    cs10_deltas = ArrayField(models.IntegerField(), null=True)
    skill_order = ArrayField(models.CharField(max_length=1), null=True)

    date_created = models.DateTimeField(auto_now_add=True, blank=False)

    def __str__(self):
        return str(self.match) + ': ' + str(self.summoner)


class ParticipantFrame(models.Model):
    match = models.ForeignKey(Match, related_name='Participant_Match', on_delete=models.CASCADE, blank=False, null=False)
    participant_id = models.IntegerField(null=False, blank=False, default=0)
    total_gold = models.IntegerField(null=False, blank=False, default=0)
    level = models.IntegerField(null=False, blank=False, default=1)
    current_gold = models.IntegerField(null=False, blank=False, default=0)
    minions_killed = models.IntegerField(null=False, blank=False, default=0)
    position_x = models.IntegerField(null=True)
    position_y = models.IntegerField(null=True)
    xp = models.IntegerField(null=False, blank=False, default=0)
    jungle_minions_killed = models.IntegerField(null=False, blank=False, default=0)
    timestamp = models.IntegerField(null=False, blank=False, default=0)

    date_created = models.DateTimeField(auto_now_add=True, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['match', 'participant_id', 'timestamp'],
                                    name='Unique Participant & Timestamp by Match'),
        ]


class MatchEvent(models.Model):
    match = models.ForeignKey(Match, related_name='ParticipantEvent_Match', on_delete=models.CASCADE, blank=False, null=False)
    timestamp = models.IntegerField(null=False, blank=False, default=0)
    type = models.CharField(null=False, blank=False, max_length=255)

    participant_id = models.IntegerField(null=True)
    team_id = models.IntegerField(null=True)
    item_id = models.IntegerField(null=True)
    victim_id = models.IntegerField(null=True)
    creator_id = models.IntegerField(null=True)
    killer_id = models.IntegerField(null=True)
    assisting_participant_ids = ArrayField(models.IntegerField(), null=True)

    level_up_type = models.CharField(null=True, max_length=255)
    ward_type = models.CharField(null=True, max_length=255)
    building_type = models.CharField(null=True, max_length=255)
    monster_type = models.CharField(null=True, max_length=255)
    monster_sub_type = models.CharField(null=True, max_length=255)
    tower_type = models.CharField(null=True, max_length=255)
    lane_type = models.CharField(null=True, max_length=255)

    skill_slot = models.IntegerField(null=True)
    position_x = models.IntegerField(null=True)
    position_y = models.IntegerField(null=True)

    date_created = models.DateTimeField(auto_now_add=True, blank=False)
