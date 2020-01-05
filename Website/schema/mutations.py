import graphene
import graphql_jwt
from Website.schema.types import UserType

from Website.functions.api import get_summoner
from Website.functions.game_data import update_game_data
from Website.functions.general import account_activation_token, generate_early_access_code
from Website.tasks import send_early_access_email
from Website.schema.types import SummonerType, UserNode, ProfileType, NotificationType
from django.db import IntegrityError
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from datetime import datetime


class AcceptEarlyAccessApplication(graphene.Mutation):
    class Arguments:
        application_id = graphene.Int()

    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info, application_id):
        from Website.models import RegistrationInterest
        application = RegistrationInterest.objects.get(id=application_id)

        application.accepted = True
        application.early_access_key = generate_early_access_code(application=application)
        application.save()

        send_early_access_email.delay({
            'name': application.name,
            'email': application.email,
            'key': application.early_access_key.key
        })

        return AcceptEarlyAccessApplication(success=True)


class TogglePostLike(graphene.Mutation):
    class Arguments:
        post_id = graphene.Int()
        user_id = graphene.Int()

    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info, post_id, user_id):
        from Website.models import Post, PostInteraction, User

        post_interaction, created = PostInteraction.objects.get_or_create(
            post__id=post_id,
            user__id=user_id,
            defaults={
                'user': User.objects.get(id=user_id),
                'post': Post.objects.get(id=post_id),
                'post_interaction_type': 1
            }
        )

        if not created:
            post_interaction.post_interaction_type = 2 if post_interaction.post_interaction_type == 1 else 1

        post_interaction.save()

        return TogglePostLike(success=True)


class MarkNotificationSeen(graphene.Mutation):
    class Arguments:
        notification_id = graphene.Int()
        mark_all = graphene.Boolean()

    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info, notification_id, mark_all):
        from Website.models import Notification

        if mark_all:
            notifications = Notification.objects.filter(seen=False)

            for notification in notifications:
                notification.seen = True

            Notification.objects.bulk_update(notifications, ['seen', ])
        else:
            notification = Notification.objects.get(id=notification_id)
            notification.seen = True
            notification.save()

        return MarkNotificationSeen(success=True)


class CreateNotification(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        content = graphene.String()
        category = graphene.String()
        userId = graphene.Int()

    notification = graphene.Field(NotificationType)
    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info, title, content, category, userId):
        from Website.models import Notification
        from django.contrib.auth.models import User

        try:
            notification = Notification.objects.create(
                title=title,
                content=content,
                category=category,
                user=User.objects.get(id=userId)
            )
        except:
            return CreateNotification(notification=None, success=False)

        return CreateNotification(notification=notification, success=True)


class RegisterInterest(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        email = graphene.String()

    success = graphene.Boolean()
    errorReason = graphene.String()

    @staticmethod
    def mutate(root, info, name, email):
        from Website.models import RegistrationInterest
        obj, created = RegistrationInterest.objects.get_or_create(
            email=email,
            defaults={
                'name': name,
                'email': email
            }
        )
        if created:
            return RegisterInterest(success=True, errorReason=None)
        else:
            return RegisterInterest(success=False, errorReason='This email is already registered for early access.')


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
        update_game_data('9.22.1')

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


class RegisterInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    key = graphene.String(required=True)


class Register(graphene.Mutation):
    class Arguments:
        input = RegisterInput()

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    @staticmethod
    def mutate(root, info, input):
        from Website.models import AccessCode, User
        try:
            access_key = AccessCode.objects.get(key=input.key)
            if User.objects.filter(username__iexact=input.username).count() == 0:
                if not access_key.used and (not access_key.registration_interest or access_key.registration_interest.email == input.email):
                    try:
                        # Create the new user.
                        user = User.objects.create(
                            username=input.username,
                            email=input.email,
                            is_active=True
                        )
                        user.set_password(input.password)
                        user.save()

                        # Deactivate the Access Key used.
                        access_key.used = True
                        access_key.archived = True
                        access_key.user = user
                        access_key.date_used = datetime.now()
                        access_key.save()

                        if not access_key.registration_interest:
                            # Send confirmation email.
                            mail_subject = 'Welcome to Ally! Let\'s activate your account.'
                            mail_plain = render_to_string('Website/email/email_confirmation.txt', {
                                'user': user,
                                'domain': 'api.ally.gg',
                                'username': user.username,
                                'token': account_activation_token.make_token(user),
                            })
                            mail_html = render_to_string('Website/email/email_confirmation.html', {
                                'user': user,
                                'domain': 'api.ally.gg',
                                'username': user.username,
                                'token': account_activation_token.make_token(user),
                            })
                            send_mail(
                                mail_subject,  # Email subject.
                                mail_plain,  # Email plaintext.
                                'noreply@ally.gg',  # Email 'From' address.
                                [user.email, ],  # Email 'To' addresses. This must be a list or tuple.
                                html_message=mail_html,  # Email in HTML.
                            )
                        return Register(success=bool(user.id))

                    except IntegrityError:
                        errors = ["email", "Email already registered."]
                        return Register(success=False, errors=errors)

                else:
                    errors = ["key", "Access Key has already been used."]
                    return Register(success=False, errors=errors)
            else:
                errors = ["username", "Username is taken."]
                return Register(success=False, errors=errors)

        except AccessCode.DoesNotExist:
            errors = ["key", "Access Key does not exist."]
            return Register(success=False, errors=errors)


class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)
    expires = graphene.DateTime()

    @classmethod
    def resolve(cls, root, info, **kwargs):

        return cls(user=info.context.user)


class CreateAccessKey(graphene.Mutation):
    key = graphene.String()

    @staticmethod
    def mutate(root, info):
        return CreateAccessKey(key=generate_early_access_code().key)


class VerifySummoner(graphene.Mutation):
    class Arguments:
        summoner_name = graphene.String()
        server = graphene.String()
        user_id = graphene.Int()

    success = graphene.Boolean()
    message = graphene.String()
    summoner = graphene.Field(SummonerType)

    @staticmethod
    def mutate(root, info, summoner_name, server, user_id):
        from Website.functions.api import riot_api, get_summoner
        from Website.models import Summoner, Profile

        try:
            summoner = Summoner.objects.get(summoner_name=summoner_name)
        except:
            summoner = get_summoner(summoner_name, server)['summoner']

        response = riot_api(server, 'platform', 'v4', 'third-party-code/by-summoner/' + summoner.summoner_id)
        print(response)

        if 'error' not in response:
            try:
                profile = Profile.objects.get(user__id=user_id)
            except:
                return VerifySummoner(
                    success=False,
                    message=f'No user with the id of {user_id} was found.',
                    summoner=None
                )

            if profile.third_party_token == response:
                summoner.user_profile = profile
                summoner.save()

                if profile.main_summoner is None:
                    profile.main_summoner = summoner
                    profile.save()

                return VerifySummoner(
                    success=True,
                    message=f'Summoner successfully verified.',
                    summoner=summoner
                )
            else:
                # Error: Token returned was incorrect.
                return VerifySummoner(
                    success=False,
                    message=f'Incorrect Token. API returned {response}',
                    summoner=None
                )

        else:
            # Error: API call failed.
            return VerifySummoner(
                success=False,
                message=f'Riot API returned error: {response["message"]}.',
                summoner=None
            )



