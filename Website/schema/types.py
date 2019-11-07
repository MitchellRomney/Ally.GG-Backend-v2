import graphene
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from graphene_django.types import DjangoObjectType
from graphql_jwt.utils import jwt_encode, jwt_payload

from Website.models import Summoner


class UserType(DjangoObjectType):
    class Meta:
        model = User


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
