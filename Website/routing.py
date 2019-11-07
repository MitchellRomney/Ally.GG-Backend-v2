from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('summoner/<server>/<summonerId>', consumers.SummonerConsumer),
]
