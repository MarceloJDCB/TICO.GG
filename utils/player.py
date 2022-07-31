import json

from integrations.services.riotlolapi import RiotLolService
from ticorequests import models
from .champion import Champion, ChampionList
from .match import MatchUtils
from .dictToJson import dictToJson

class PlayerUtil:
    def __init__(self,player_name: str):
        self.player = models.PlayerObject.objects.get(name=player_name)

    def get_champion_statistics(self):
        matchs_queryset = models.MatchObject.objects.all()
        new_champions = []
        for match in matchs_queryset:
            match_data = MatchUtils(match.match_id).get_match_json()
            if match_data['category'] == "Ranked Solo":
                for participant in match_data['participants']:
                    if participant['puuid'] == self.player.puuid:
                        new_champions.append(
                            Champion(participant['champion'],
                                    participant['kills'],
                                    participant['deaths'],
                                    participant['assists'],
                                    participant['win'],
                                    float(participant['cs']),
                                    float(
                                        match_data['gameDuration'].replace(":",".")
                                    )))
        def get_champion_name(champion):
            return champion.name
        new_champions.sort(key=get_champion_name)
        return ChampionList(new_champions).generate_champions_statistics()
    
    def get_solo_league_info(self):
        league_response = RiotLolService().get_leaguev4(self.player.summoner_id).json()
        queues_info = []
        for league_info in league_response:
            queue = league_info['queueType']
            if(queue != "RANKED_TFT_PAIRS"):
                league_id = league_info['leagueId']
                tier = league_info['tier']
                rank = league_info['rank']
                league_points = json.dumps(league_info['leaguePoints'])
                wins = json.dumps(league_info['wins'])
                losses = json.dumps(league_info['losses'])
                wins = league_info['wins']
                totalmatchs = wins + league_info['losses']
                winrate = json.dumps(round((wins / totalmatchs) * 100, 1))
                ranked_info = {
                    "league_id": league_id,
                    "queue":queue,
                    "tier":tier,
                    "rank":rank,
                    "league_points":league_points,
                    "wins":str(wins),
                    "losses":losses,
                    "winrate": winrate
                }
                queues_info.append(ranked_info)
        return queues_info

    def get_player_json(self):
        return {
                "puuid": self.player.puuid,
                "summonerid": self.player.summoner_id,
                "name": self.player.name,
                "icon": self.player.icon,
                "level": self.player.level,
                "ranked": self.format_ranked_textfield(),
                "matchs": self.format_matchs_textfield(),
                "championStatistics": self.format_championtatistics_textfield()
            }

    def format_ranked_textfield(self):
        return dictToJson(self.player.ranked_solo)

    def format_matchs_textfield(self):
        return dictToJson(self.player.matchs)
    
    def format_championtatistics_textfield(self):
        return dictToJson(self.player.championStatistics)