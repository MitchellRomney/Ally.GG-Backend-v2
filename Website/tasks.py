from __future__ import absolute_import, unicode_literals

import json

from asgiref.sync import async_to_sync
from celery.signals import celeryd_init
from channels.layers import get_channel_layer

from AllyBackend import schema
from AllyBackend.celery import app
from Website.functions.api import get_latest_version, get_match, get_summoner
from Website.functions.game_data import update_game_data


@celeryd_init.connect
def startup_tasks(sender=None, conf=None, **kwargs):

    # Clean out old queue
    app.control.purge()

    # Update the game data on startup.
    update_game_data(get_latest_version())
    print('Ally is started and ready to receive tasks!')


@app.task
def update_summoner(summoner_id, server):
    get_summoner(summoner_id=summoner_id, server=server)

    room_group_name = f'summoner_{server}_{summoner_id}'

    result = schema.schema.execute(
        '''
        {{
          summoner(summonerId: "{summoner_id}", server: "{server}") {{
              summonerId
              server
              summonerName
              profileIconId
              summonerLevel
              lastUpdated
              rankedSolo {{
                tier
                rank
                rankNumber
                lp
                leagueName
                wins
                losses
                ringValues
              }}
              rankedFlex5 {{
                tier
                rank
                rankNumber
                lp
                leagueName
                wins
                losses
                ringValues
              }}
              rankedFlex3 {{
                tier
                rank
                rankNumber
                lp
                leagueName
                wins
                losses
                ringValues
              }}
            }}
        }}
        '''.format(summoner_id=summoner_id, server=server)
    )

    async_to_sync(get_channel_layer().group_send)(
        room_group_name,
        {
            'type': 'celery',
            'message': 'Summoner Updated!',
            'data': {
                'summoner': json.dumps(result.data)
            }
        }
    )

    return True


@app.task
def fetch_match(game_id, summoner_id, server):
    result = get_match(game_id, server)

    room_group_name = 'summoner_{0}_{1}'.format(server, summoner_id)

    result = schema.schema.execute(
        '''
        {{
          player(summonerId: "{summoner_id}", gameId: {gameId}, server: "{server}") {{
            match {{
              gameId
              queue
              gameDurationTime
              timeago
              timestamp
              players {{
                participantId
                champion {{
                  champId
                  name
                }}
                team {{
                  teamId
                }}
                summoner {{
                  summonerName
                  rankedSolo {{
                    tier
                    rank
                    rankNumber
                    lp
                    leagueName
                    wins
                    losses
                    ringValues
                  }}
                  rankedFlex5 {{
                    tier
                    rank
                    rankNumber
                    lp
                    leagueName
                    wins
                    losses
                    ringValues
                  }}
                  rankedFlex3 {{
                    tier
                    rank
                    rankNumber
                    lp
                    leagueName
                    wins
                    losses
                    ringValues
                  }}
                }}
              }}
            }}
            champion {{
              key
              name
              champId
            }}
            lane
            laneOpponent {{
              champion {{
                key
                name
                champId
              }}
            }}
            win
            kills
            deaths
            assists
            kdaAverage
            champLevel
            killParticipation
            totalMinionsKilled
            neutralMinionsKilled
            csPmin
            item0 {{
              itemId
              name
            }}
            item1 {{
              itemId
              name
            }}
            item2 {{
              itemId
              name
            }}
            item3 {{
              itemId
              name
            }}
            item4 {{
              itemId
              name
            }}
            item5 {{
              itemId
              name
            }}
            item6 {{
              itemId
              name
            }}
            spell1Id {{
              name
              imageFull
            }}
            spell2Id {{
              name
              imageFull
            }}
            perk0 {{
              name
              icon
            }}
            perkSubStyle
            perk4 {{
              name
            }}
          }}
        }}
        '''.format(summoner_id=summoner_id, gameId=game_id, server=server)
    )

    async_to_sync(get_channel_layer().group_send)(
        room_group_name,
        {
            'type': 'celery',
            'message': 'New match added: ' + str(game_id),
            'data': {
                'match': json.dumps(result.data)
            }
        }
    )

    return True
