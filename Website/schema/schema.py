import graphene
import graphql_jwt

from Website.schema.mutations import FetchMatches, FetchSummoner, UpdateGameData, Login, ObtainJSONWebToken, \
    EditProfile, RegisterInterest, Register, CreateAccessKey, VerifySummoner, CreateNotification, \
    MarkNotificationSeen, TogglePostLike, AcceptEarlyAccessApplication
from Website.schema.types import UserType, SummonerType, ParticipantType, ProfileType, AccessKeyType, \
    NotificationType, PostType, RegistrationInterestType
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

    user_notifications = graphene.List(
        NotificationType,
        user_id=graphene.Int()
    )

    participant = graphene.Field(
        ParticipantType,
        game_id=graphene.Int(),
        summoner_id=graphene.String(),
        server=graphene.String()
    )

    summoner = graphene.Field(
        SummonerType,
        server=graphene.String(),
        summoner_name=graphene.String()
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

    posts = graphene.List(
        PostType,
        user_id=graphene.Int()
    )

    registration_interests = graphene.List(
        RegistrationInterestType
    )

    @staticmethod
    def resolve_posts(self, info, **kwargs):
        from Website.models import Post, Profile, PostInteraction
        user_id = kwargs.get('user_id')
        profile = Profile.objects.filter(user__id=user_id)
        followed_user_ids = list(profile.values_list('following__id', flat=True))
        followed_user_ids.append(user_id)
        posts = Post.objects.filter(user_source__id__in=followed_user_ids).order_by('-date_created')[:10]
        existing_likes = list(PostInteraction.objects.filter(post_interaction_type=1, user__id=user_id, post__id__in=list(posts.values_list('id', flat=True))).values_list('post__id', flat=True))
        for p in posts:
            p.userLiked = p.id in existing_likes
        return posts

    @staticmethod
    def resolve_user(self, info, **kwargs):
        return User.objects.get(id=kwargs.get('user_id')) if kwargs.get('user_id') is not None else \
            User.objects.get(username__iexact=kwargs.get('username'))

    @staticmethod
    def resolve_registration_interests(self, info, **kwargs):
        from Website.models import RegistrationInterest
        return RegistrationInterest.objects.all().order_by('-date_created')

    @staticmethod
    def resolve_user_summoners(self, info, **kwargs):
        from Website.models import Summoner
        return Summoner.objects.filter(user_profile__user__id=kwargs.get('user_id')).select_related('user_profile')

    @staticmethod
    def resolve_user_notifications(self, info, **kwargs):
        from Website.models import Notification
        return Notification.objects.filter(user__id=kwargs.get('user_id')).order_by('-date_created')[:10]

    @staticmethod
    def resolve_participant(self, info, **kwargs):
        from Website.models import Participant
        return Participant.objects.get(match__game_id=kwargs.get('game_id'), summoner__server=kwargs.get('server'), summoner__summoner_id=kwargs.get('summoner_id'))

    @staticmethod
    def resolve_summoner(self, info, **kwargs):
        from Website.models import Summoner
        return Summoner.objects.get(server=kwargs.get('server'), summoner_name__iexact=kwargs.get('summoner_name'))

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
    create_notification = CreateNotification.Field()
    mark_notification_seen = MarkNotificationSeen.Field()
    toggle_post_like = TogglePostLike.Field()
    accept_early_access_application = AcceptEarlyAccessApplication.Field()

