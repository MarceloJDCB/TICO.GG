import requests
from .tasks import API_KEY
def checkConnection(player_name):
    URL = "https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + player_name + \
          "?api_key=" + API_KEY
    status_code = requests.get(URL).status_code
    if status_code == 200:
        return True
    else:
        return False