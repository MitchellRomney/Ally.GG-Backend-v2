import graphene
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models import Sum
from graphene_django.types import DjangoObjectType
from graphql_jwt.utils import jwt_encode, jwt_payload

from Website.models import Summoner, RankedTier, Participant, Champion, Match, Item, Rune, SummonerSpell, Team, Profile, RegistrationInterest, AccessCode


class RegistrationInterestType(DjangoObjectType):
    class Meta:
        model = RegistrationInterest


class AccessKeyType(DjangoObjectType):
    class Meta:
        model = AccessCode


class ItemType(DjangoObjectType):
    class Meta:
        model = Item


class RuneType(DjangoObjectType):
    class Meta:
        model = Rune


class SummonerSpellType(DjangoObjectType):
    class Meta:
        model = SummonerSpell


class Build(graphene.ObjectType):
    trinket = graphene.Field(ItemType)
    slot1 = graphene.Field(ItemType)
    slot2 = graphene.Field(ItemType)
    slot3 = graphene.Field(ItemType)
    slot4 = graphene.Field(ItemType)
    slot5 = graphene.Field(ItemType)
    slot6 = graphene.Field(ItemType)
    spell1 = graphene.Field(SummonerSpellType)
    spell2 = graphene.Field(SummonerSpellType)


class UserType(DjangoObjectType):
    class Meta:
        model = User


class RankedTierType(DjangoObjectType):
    class Meta:
        model = RankedTier


class SummonerType(DjangoObjectType):
    class Meta:
        model = Summoner


class UserNode(DjangoObjectType):
    token = graphene.String()

    class Meta:
        model = get_user_model()
        filter_fields = [
            'username',
        ]

    def resolve_token(self, info, **kwargs):
        if info.context.user != self:
            return None

        payload = jwt_payload(self)
        return jwt_encode(payload)


class ParticipantType(DjangoObjectType):
    class Meta:
        model = Participant

    creep_score = graphene.Int()
    creep_score_average = graphene.Float()
    kda_average = graphene.Float()
    kill_participation = graphene.String()
    build = graphene.Field(Build)
    result = graphene.String()

    def resolve_creep_score(self, info):
        return self.total_minions_killed + self.neutral_minions_killed

    def resolve_creep_score_average(self, info):
        total_minions = self.total_minions_killed + self.neutral_minions_killed
        duration_seconds = self.match.game_duration % 60
        duration_minutes = (self.match.game_duration - duration_seconds) / 60
        return round(total_minions / (duration_minutes + (duration_seconds / 60)), 1) if total_minions > 0 else 0.0

    def resolve_kill_participation(self, info):
        total_kills = Participant.objects \
            .filter(match=self.match, team=self.team) \
            .aggregate(Sum('kills')).get('kills__sum', 0)
        return str(int(((self.kills + self.assists) / total_kills) * 100)) + '%' if total_kills != 0 else '0%'

    def resolve_kda_average(self, info):
        average = (self.kills + self.assists) / self.deaths if self.deaths != 0 else self.kills + self.assists
        return round(average, 2)

    def resolve_build(self, info):
        return Build(trinket=self.item6, slot1=self.item0, slot2=self.item1, slot3=self.item2, slot4=self.item3,
                     slot5=self.item4, slot6=self.item5, spell1=self.spell1_id, spell2=self.spell2_id)

    def resolve_result(self, info):
        winning_team = Team.objects.get(match=self.match, win=True)
        result = 'Victory' if self.win else 'Defeat'
        return 'Remake' if self.match.game_duration < 300 and winning_team.inhibitor_kills == 0 else result


class ChampionType(DjangoObjectType):
    class Meta:
        model = Champion


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile


class MatchType(DjangoObjectType):
    queue = graphene.String()
    game_length = graphene.String()

    class Meta:
        model = Match

    def resolve_queue(self, info):
        return self.get_queue_id_display()

    def resolve_game_length(self, info):
        duration_seconds = self.game_duration % 60
        duration_minutes = (self.game_duration - duration_seconds) / 60
        return str(int(duration_minutes)) + 'm ' + str(duration_seconds) + 's '
