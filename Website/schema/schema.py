import graphene
import graphql_jwt

from Website.schema.mutations import FetchMatches, FetchSummoner, UpdateGameData, Login, ObtainJSONWebToken, \
    EditProfile, RegisterInterest, Register, CreateAccessKey, VerifySummoner
from Website.schema.types import UserType, SummonerType, ParticipantType, ProfileType, AccessKeyType
from django.contrib.auth.models import User


class Query(object):
    user = graphene.Field(
        UserType,
        user_id=graphene.Int(),
        username=graphene.String())

    user_summoners = graphene.List(
        SummonerType,
        user_id=graphene.Int()
    )

    summoner_participants = graphene.List(
        ParticipantType,
        games=graphene.Int(),
        summoner_id=graphene.String(),
        server=graphene.String()
    )

    profile = graphene.Field(
        ProfileType,
        user_id=graphene.Int()
    )

    key = graphene.Field(
        AccessKeyType,
        key=graphene.String()
    )

    @staticmethod
    def resolve_user(self, info, **kwargs):
        return User.objects.get(id=kwargs.get('user_id')) if kwargs.get('user_id') is not None else \
            User.objects.get(username=kwargs.get('username'))

    @staticmethod
    def resolve_user_summoners(self, info, **kwargs):
        from Website.models import Summoner
        return Summoner.objects.filter(user_profile__user__id=kwargs.get('user_id')).select_related('user_profile')

    @staticmethod
    def resolve_summoner_participants(self, info, **kwargs):
        from Website.models import Participant
        return Participant.objects \
                   .filter(summoner__summoner_id=kwargs.get('summoner_id'), summoner__server=kwargs.get('server')) \
                   .select_related('champion', 'summoner', 'match', 'item0', 'item1', 'item2', 'item3', 'item4',
                                   'item5', 'item6').order_by('-match__timestamp')[:kwargs.get('games')]

    @staticmethod
    def resolve_profile(self, info, **kwargs):
        from Website.models import Profile
        from Website.functions.general import generate_summoner_verification_code

        user_id = kwargs.get('user_id')

        try:
            user_profile = Profile.objects.get(user__id=user_id)

            if user_profile.third_party_token is None:
                user_profile.third_party_token = generate_summoner_verification_code()
                user_profile.save()

            return user_profile
        except:
            return None

    @staticmethod
    def resolve_key(self, info, **kwargs):
        from Website.models import AccessCode

        key = kwargs.get('key')

        if key:
            return AccessCode.objects.get(key=key)


class Mutation(graphene.ObjectType):
    fetch_summoner = FetchSummoner.Field()
    fetch_matches = FetchMatches.Field()
    update_game_data = UpdateGameData.Field()
    edit_profile = EditProfile.Field()
    register_interest = RegisterInterest.Field()
    create_access_key = CreateAccessKey.Field()
    register = Register.Field()
    token_auth = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    login = Login.Field()
    verify_summoner = VerifySummoner.Field()

