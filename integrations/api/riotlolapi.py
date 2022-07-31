from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
import requests

from integrations.config.riotlolapi import RiotApiConfig
from integrations.models.riot import BaseApiCall

class RiotLolApi:
    def __init__(self):
        self.riot_config = RiotApiConfig()

    def get_summoner_v4(self,player):
        url = f"{self.riot_config.br1_base_api_link}/summoner/v4/summoners/by-name/{player}"
        return self.riot_request(url,'','GET')
    
    def get_league_v4(self,player_id):
        url = f"{self.riot_config.br1_base_api_link}/league/v4/entries/by-summoner/{player_id}"
        return self.riot_request(url,'','GET')
    
    def get_matchv5_timeline(self,match_id):
        url = f"{self.riot_config.america_base_api_link}/match/v5/matches/{match_id}/timeline"
        return self.riot_request(url,'','GET')
    
    def get_matchv5(self,match_id):
        url = f"{self.riot_config.america_base_api_link}/match/v5/matches/{match_id}"
        return self.riot_request(url,'','GET')
    
    def get_mathv5_list(self,player_puuid):
        url = f"{self.riot_config.america_base_api_link}/match/v5/matches/by-puuid/{player_puuid}/ids?start=0&count={settings.PLAYER_MATCH_COUNT}"
        return self.riot_request(url,'','GET')

    def get_leaguev4(self,player_puuid):
        url = f"{self.riot_config.br1_base_api_link}/league/v4/entries/by-summoner/{player_puuid}"
        return self.riot_request(url,'','GET')

    def get_summonnerv4(self,player_name):
        url = f"{self.riot_config.br1_base_api_link}/summoner/v4/summoners/by-name/{player_name}"
        return self.riot_request(url,'','GET')


    def riot_request(self,url,data,method):
        headers = {
            "Content-Type": "application/json",
            "X-Riot-Token": self.riot_config.riot_api_token
        }
        try:
            response = requests.request(
                method,
                url,
                data=data,
                headers=headers
            )

            if response.status_code in [200,201]:
                BaseApiCall.objects.create(
                    api="RIOT",
                    method=method,
                    url=url,
                    data=data,
                    success=True,
                    response_status_code=response.status_code,
                    response_data=response.json()
                )
            else:
                BaseApiCall.objects.create(
                    api="RIOT",
                    method=method,
                    url=url,
                    data=data,
                    success=False,
                    response_status_code=response.status_code,
                    response_data=response.json()
                )
        except Exception as er:
            BaseApiCall.objects.create(
                    api="RIOT",
                    method=method,
                    url=url,
                    data=data,
                    success=False,
                    response_status_code=response.status_code or None,
                    response_data=f"{er} / {response.json()}"
                )

        return response
