import graphene
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models import Sum
from graphene_django.types import DjangoObjectType
from graphql_jwt.utils import jwt_encode, jwt_payload

from Website.models import Summoner, RankedTier, Participant, Champion, Match, Item, Rune, SummonerSpell, \
    Team, Profile, RegistrationInterest, AccessCode, Notification, Post, PostInteraction


class PostType(DjangoObjectType):
    class Meta:
        model = Post

    like_count = graphene.Int()
    user_liked = graphene.Boolean()
    type = graphene.String()

    @staticmethod
    def resolve_like_count(self, info):
        return PostInteraction.objects.filter(post__id=self.id, post_interaction_type=1).count()

    @staticmethod
    def resolve_user_liked(self, info, **kwargs):
        return self.userLiked

    @staticmethod
    def resolve_type(self, info, **kwargs):
        return self.get_post_type_display()


class PostInteractionType(DjangoObjectType):
    class Meta:
        model = PostInteraction


class NotificationType(DjangoObjectType):
    class Meta:
        model = Notification


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


class StatisticsType(graphene.ObjectType):
    winrate = graphene.Int()


class SummonerType(DjangoObjectType):
    statistics = graphene.Field(StatisticsType)

    class Meta:
        model = Summoner

    @staticmethod
    def resolve_statistics(self, info, **kwargs):
        from Website.models import Participant
        latest_games = Participant.objects.filter(summoner__id=self.id).order_by('-match__timestamp')[:20]
        win_count = 0
        for game in latest_games:
            if game.win:
                win_count += 1
        return StatisticsType(winrate=round((win_count/20)*100))


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
