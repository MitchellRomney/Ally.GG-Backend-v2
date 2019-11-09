import graphene
import graphql_jwt

from Website.schema.mutations import FetchMatches, FetchSummoner, UpdateGameData, Login, ObtainJSONWebToken
from Website.schema.types import UserType, SummonerType, ParticipantType
from django.contrib.auth.models import User


class Query(object):
    user = graphene.Field(UserType, user_id=graphene.Int())

    @staticmethod
    def resolve_user(self, info, **kwargs):
        return User.objects.get(id=kwargs.get('user_id')) if kwargs.get('user_id') is not None else \
            User.objects.get(username=kwargs.get('username'))

    user_summoners = graphene.List(SummonerType, user_id=graphene.Int())

    @staticmethod
    def resolve_user_summoners(self, info, **kwargs):
        from Website.models import Summoner
        return Summoner.objects.filter(user_profile__user__id=kwargs.get('user_id')).select_related('user_profile')

    summoner_participants = graphene.List(ParticipantType,
                                          games=graphene.Int(),
                                          summoner_id=graphene.String(),
                                          server=graphene.String())

    @staticmethod
    def resolve_summoner_participants(self, info, **kwargs):
        from Website.models import Participant
        return Participant.objects \
                   .filter(summoner__summoner_id=kwargs.get('summoner_id'),summoner__server=kwargs.get('server')) \
                   .select_related('champion', 'summoner', 'match', 'item0', 'item1', 'item2', 'item3', 'item4',
                                   'item5', 'item6').order_by('-match__timestamp')[:kwargs.get('games')]


class Mutation(graphene.ObjectType):
    fetch_summoner = FetchSummoner.Field()
    fetch_matches = FetchMatches.Field()
    update_game_data = UpdateGameData.Field()
    token_auth = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    login = Login.Field()
