from ticorequests.models import PlayerObject
from .dictToJson import dictToJson

class PlayerUtil:
    def __init__(self,player_name: str):
        self.player = PlayerObject.objects.get(name=player_name)

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