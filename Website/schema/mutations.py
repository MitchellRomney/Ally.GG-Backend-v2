import graphene
import graphql_jwt
from Website.schema.types import UserType

from Website.functions.api import get_summoner
from Website.functions.game_data import update_game_data
from Website.schema.types import SummonerType, UserNode, ProfileType
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login


class FetchSummoner(graphene.Mutation):
    class Arguments:
        summoner_name = graphene.String()
        server = graphene.String()

    summoner = graphene.Field(SummonerType)
    created = graphene.Boolean()

    @staticmethod
    def mutate(root, info, summoner_name, server):

        # Fetch & save the Summoner from the Riot API.
        response = get_summoner(summoner_name=summoner_name, server=server)

        return FetchSummoner(summoner=response['summoner'], created=response['created'])


class EditProfile(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int()
        main_summoner = graphene.String()

    profile = graphene.Field(ProfileType)

    @staticmethod
    def mutate(root, info, user_id, main_summoner):
        from Website.models import Profile, Summoner
        profile = Profile.objects.get(user__id=user_id)

        if main_summoner:
            profile.main_summoner = Summoner.objects.get(summoner_id=main_summoner)

        profile.save()
        return EditProfile(profile=profile)


class FetchMatches(graphene.Mutation):
    class Arguments:
        summoner_id = graphene.String()
        server = graphene.String()
        games = graphene.Int()
        fetch_all = graphene.Boolean()

    new_matches = graphene.Int()

    @staticmethod
    def mutate(root, info, summoner_id, server, games, fetch_all):
        from Website.functions.api import get_match_list
        from Website.tasks import fetch_match
        from Website.models import Match

        match_list = [match['gameId'] for match in get_match_list(summoner_id, server, games, fetch_all)]
        existing_matches = list(Match.objects.filter(game_id__in=match_list).values_list('game_id', flat=True))
        new_matches = [x for x in match_list if x not in existing_matches]

        for match_id in new_matches:
            fetch_match.delay(match_id, summoner_id, server)

        return FetchMatches(new_matches=len(new_matches))


class UpdateGameData(graphene.Mutation):
    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info):
        update_game_data('9.21.1')

        return UpdateGameData(success=True)


class Login(graphene.Mutation):
    user = graphene.Field(UserNode)

    class Arguments:
        username = graphene.String()
        password = graphene.String()

    @classmethod
    def mutate(cls, root, info, username, password):
        user_model = get_user_model()

        user_obj = user_model.objects.get(username__iexact=username)

        user = authenticate(username=user_obj.username, password=password)

        if user is None:
            raise Exception('Please enter a correct username and password')

        if not user.is_active:
            raise Exception('It seems your account has been disabled')

        login(info.context, user)

        return cls(user=user)


class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)
    expires = graphene.DateTime()

    @classmethod
    def resolve(cls, root, info, **kwargs):

        return cls(user=info.context.user)
