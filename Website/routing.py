from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('notifications/<userId>', consumers.NotificationsConsumer),
    path('summoner/<server>/<summonerId>', consumers.SummonerConsumer)
]
