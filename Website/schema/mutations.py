import graphene
import graphql_jwt
from Website.schema.types import UserType

from Website.functions.api import get_summoner
from Website.functions.game_data import update_game_data
from Website.functions.general import account_activation_token, generate_early_access_code
from Website.schema.types import SummonerType, UserNode, ProfileType
from django.db import IntegrityError
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from datetime import datetime


class RegisterInterest(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        email = graphene.String()

    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info, name, email):
        from Website.models import RegistrationInterest
        RegistrationInterest.objects.create(first_name=name, email=email)

        return RegisterInterest(success=True)


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

            if access_key.used is False:
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

                    # TODO: If DEBUG ignore email

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
        return CreateAccessKey(key=generate_early_access_code())


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



