from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from AllyBackend.views import activate

from AllyBackend.schema import schema

urlpatterns = [
    path('', admin.site.urls),
    path('activate/<username>/<token>', activate, name='activate'),
    path('graphql', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]
