
class Champion:
    def __init__(self, name, kill, death, assist, win, cs, game_duration):
        self.name = name
        self.kill = float(kill)
        self.death = float(death)
        self.assist = float(assist)
        self.win = win
        self.cs = cs
        self.game_duration = game_duration
    
class ChampionList:
    def __init__(self, foreign_champion_list):
        self.foreign_champion_list = foreign_champion_list
        self.champions = []
    
    def statistic_dict(self, name, kill, death, assist, cs , game_duration, win):
        champion_dict =  {
                "champion":name,
                "kills":kill,
                "deaths":death,
                "assists":assist,
                "cs":cs,
                "game_duration":game_duration,
                "wins":0,
                "losses":0,
                "winrate":0,
                "kda":0,
                "qnty":1
            }
        if bool(win): champion_dict['wins'] += 1
        else: champion_dict['losses'] += 1
        return champion_dict
        
    def sum_statistic_obj(self,champion,previous_champ):
        previous_champ['kills'] +=  champion.kill
        previous_champ['deaths'] += champion.death
        previous_champ['assists'] += champion.assist
        previous_champ['cs'] += champion.cs
        previous_champ['game_duration'] += champion.game_duration
        if champion.win == "true": previous_champ['wins'] += 1
        else: previous_champ['losses'] += 1
        previous_champ['qnty'] += 1
        return previous_champ


    def sum_champions_statistics(self):
        num_champion = 0
        for champion in self.foreign_champion_list:
            print(champion.name)
            if num_champion > 0:
                previous_champ = self.champions[num_champion - 1]
                if champion.name == previous_champ['champion']:
                    previous_champ = self.sum_statistic_obj(champion,previous_champ)
                    continue
            self.champions.append(self.statistic_dict(
                champion.name,
                champion.kill,
                champion.death,
                champion.assist,
                champion.cs,
                champion.game_duration,
                champion.win
            ))
            num_champion += 1

    def division_and_round(self,num,num_2):
        if num_2 == 0:
            return round(num, 1)
        return round(num / num_2, 1)

    def division_multiply_and_round(self,num,num_2):
        if num_2 == 0:
            return round(num * 100, 1)
        return round((num / num_2) * 100, 1)

    def champion_kda(self,champion):
        champion['kda'] = champion['assists'] +  champion['kills']
        if champion['deaths'] > 0:
            champion['kda'] /= champion['deaths']
        champion['kda'] = round(champion['kda'],1)

    def calculate_the_statistics(self):
        for champion in self.champions:
            champion['kills'] = self.division_and_round(champion['kills'],champion['qnty'])
            champion['deaths'] = self.division_and_round(champion['deaths'],champion['qnty'])
            champion['assists'] = self.division_and_round(champion['assists'],champion['qnty'])
            champion['cs'] = self.division_and_round(champion['cs'],champion['game_duration'])
            champion['game_duration'] = self.division_and_round(champion['game_duration'],60)
            champion['winrate'] = self.division_multiply_and_round(champion['wins'] , champion['qnty'])
            self.champion_kda(champion)

    def convert_camps_to_string(self):
        for champion in self.champions:
            champion['kills'] = str(champion['kills'])
            champion['deaths'] = str(champion['deaths'])
            champion['assists'] = str(champion['assists'])
            champion['kda'] = str(champion['kda'])
            champion['cs'] = str(champion['cs'])
            champion['game_duration'] = str(champion['game_duration'])
            champion['wins'] = str(champion['wins'])
            champion['losses'] = str(champion['losses'])
            champion['qnty'] = str(champion['qnty'])
            champion['winrate'] = str(champion['winrate'])

    def generate_champions_statistics(self):
        self.sum_champions_statistics()    
        self.calculate_the_statistics()
        self.convert_camps_to_string()
        return self.champions
