from integrations.api.riotlolapi import RiotLolApi

class RiotLolService:
    def __init__(self):
        self.riot_api = RiotLolApi()
    
    def get_player(self,player):
        return self.riot_api.get_summoner_v4(player)
    
    def get_league(self,player):
        return self.riot_api.get_league_v4(player)

    def get_matchv5_timeline(self,match_id):
        return self.riot_api.get_matchv5_timeline(match_id)
    
    def get_matchv5(self,match_id):
        return self.riot_api.get_matchv5(match_id)
    
    def get_matchv5_list(self,player_puuid):
        return self.riot_api.get_mathv5_list(player_puuid)

    def get_leaguev4(self,player_puuid):
        return self.riot_api.get_league_v4(player_puuid)
    
    def get_summonnerv4(self,player_name):
        return self.riot_api.get_summonnerv4(player_name)