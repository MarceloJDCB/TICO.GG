import requests
import random
response = requests.get('http://ddragon.leagueoflegends.com/cdn/12.7.1/data/pt_BR/champion.json').json()['data']
champions = []
for champion in response:
    champions.append(champion)
selected_champion = random.choice(champions)
print(selected_champion)