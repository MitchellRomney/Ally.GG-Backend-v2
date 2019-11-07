import graphene
import graphql_jwt

from Website.schema.mutations import FetchMatches, FetchSummoner, UpdateGameData, Login, ObtainJSONWebToken
from Website.schema.types import UserType
from django.contrib.auth.models import User


class Query(object):
    user = graphene.Field(UserType, username=graphene.String(), id=graphene.Int())

    @staticmethod
    def resolve_user(self, info, **kwargs):
        username = kwargs.get('username')
        user_id = kwargs.get('id')
        if user_id is not None:
            return User.objects.get(id=user_id)
        else:
            return User.objects.get(username=username)


class Mutation(graphene.ObjectType):
    fetch_summoner = FetchSummoner.Field()
    fetch_matches = FetchMatches.Field()
    update_game_data = UpdateGameData.Field()
    token_auth = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    login = Login.Field()
