from __future__ import absolute_import, unicode_literals
from celery import shared_task
import json
import requests
import time
import math
from .models import matchObject,playerObject,matchTimeLineObject
from celery.result import allow_join_result


# CRUCIAL PARAMETERS
API_KEY = "RGAPI-b9cf736b-5df1-4e87-af72-791949f750b1" # https://developer.riotgames.com/
PLAYER_MATCH_COUNT = 10 # DEFINES HOW MANY MATCHES THE API WILL TAKE

@shared_task
def player_champion_statistics(PUUID_player):
    class Champion:
        def __init__(self, name, kill, death, assist, win, cs, gameduration):
            self.name = name
            self.kill = float(kill)
            self.death = float(death)
            self.assist = float(assist)
            self.cs = cs
            self.gameduration = gameduration
            self.win = win

    matchs = matchObject.objects.all()
    newChamps = []
    for e in range(0,len(matchs)):
        x = {"matchid":matchs[e].matchId}
        url = "http://127.0.0.1:8000/getMatch"
        data = requests.post(url,data=x).json()
        if data['category'] == "Ranked Solo":
            for i in range(0,len(data['participants'])):
                if data['participants'][i]['puuid'] == PUUID_player:
                    name = data['participants'][i]['champion']
                    kills = data['participants'][i]['kills']
                    deaths = data['participants'][i]['deaths']
                    assists = data['participants'][i]['assists']
                    cs = float(data['participants'][i]['cs'])

                    # GAME DURATION / CATCHING ONLY THE MINUTES IN THIS ACTUAL VERSION OF TICO API
                    strgameDuration = str(data['gameDuration'])
                    gameDuration = ""
                    for y in range(0,len(strgameDuration)):
                        if strgameDuration[y] == ":":
                            break
                        else:
                            gameDuration = gameDuration + strgameDuration[y]
                    gameDuration = float(gameDuration)
                    ##################################################################
                    win = data['participants'][i]['win']
                    newChamps.append(Champion(name,kills,deaths,assists,win,cs,gameDuration))
                else:
                    continue
        else:
            continue
        
    # Ordering the champions
    def get_atr_name(c):    
        return c.name
    newList = []
    newChamps.sort(key=get_atr_name)
    for b in range(0,len(newChamps)):
        #ACTUAL
        name = newChamps[b].name
        kills = newChamps[b].kill
        deaths = newChamps[b].death
        assists = newChamps[b].assist
        cs = newChamps[b].cs
        gameduration = newChamps[b].gameduration
        win = newChamps[b].win
        if b > 0:
            #OLD
            oldname = newChamps[b-1].name
            if name == oldname:
                for z in range(0,len(newList)):
                    if newList[z]['champion'] == name:
                        newList[z]['kills'] = kills + newList[z]['kills']
                        newList[z]['deaths'] = deaths + newList[z]['deaths']
                        newList[z]['assists'] = assists + newList[z]['assists']
                        newList[z]['cs'] = cs + newList[z]['cs']
                        newList[z]['gameduration'] = gameduration + newList[z]['gameduration']
                        if win == "true":
                            newList[z]['wins'] = newList[z]['wins'] + 1
                        else:
                            newList[z]['losses'] = newList[z]['losses'] + 1
                        newList[z]['qntd'] = newList[z]['qntd'] + 1
                        break
                    else:
                        continue
            else:
                if win == "true":
                    x = {
                        "champion":name,
                        "kills":kills,
                        "deaths":deaths,
                        "assists":assists,
                        "cs":cs,
                        "gameduration":gameduration,
                        "wins":1,
                        "losses":0,
                        "winrate":0,
                        "kda":0,
                        "qntd":1
                    }
                else:
                    x = {
                    "champion":name,
                    "kills":kills,
                    "deaths":deaths,
                    "assists":assists,
                    "cs":cs,
                    "gameduration":gameduration,
                    "wins":0,
                    "losses":1,
                    "winrate":0,
                    "kda":0,
                    "qntd":1
                    }
                newList.append(x)
        else:
            if win == "true":
                x = {
                    "champion":name,
                    "kills":kills,
                    "deaths":deaths,
                    "assists":assists,
                    "cs":cs,
                    "gameduration":gameduration,
                    "wins":1,
                    "losses":0,
                    "winrate":0,
                    "kda":0,
                    "qntd":1
                }
            else:
                x = {
                "champion":name,
                "kills":kills,
                "deaths":deaths,
                "assists":assists,
                "cs":cs,
                "gameduration":gameduration,
                "wins":0,
                "losses":1,
                "winrate":0,
                "kda":0,
                "qntd":1
                }
            newList.append(x)

    for c in range(0,len(newList)):
       #VARIAVEIS PARA OPERAÇÕES MATEMÁTICAS   
        newList[c]['kills'] = (round(newList[c]['kills'] / newList[c]['qntd'], 1))
        newList[c]['deaths'] = (round(newList[c]['deaths'] / newList[c]['qntd'], 1))
        newList[c]['assists'] = (round(newList[c]['assists'] / newList[c]['qntd'], 1))
        newList[c]['cs'] = (round(newList[c]['cs'] / newList[c]['gameduration'],1))
        newList[c]['gameduration'] = (round(newList[c]['gameduration'] / 60, 1))
        newList[c]['wins'] = (newList[c]['wins'])
        newList[c]['losses'] = (newList[c]['losses'])
        newList[c]['qntd'] = (newList[c]['qntd'])
        newList[c]['winrate'] = ((newList[c]['wins'] / newList[c]['qntd']) * 100)

        # KDA (Kill/Death/Assistance) is the sum of kills and assists divided by the number of deaths
        if newList[c]['deaths'] == 0:
            newList[c]['kda'] = str(newList[c]['assists'] + newList[c]['kills'])
        else:
            newList[c]['kda'] = str((newList[c]['assists'] + newList[c]['kills']) / newList[c]['deaths'])[0:4]


        # variables that will be given to the final list
        newList[c]['kills'] = str(newList[c]['kills'])
        newList[c]['deaths'] = str(newList[c]['deaths'])
        newList[c]['assists'] = str(newList[c]['assists'])
        newList[c]['cs'] = str(newList[c]['cs'])
        newList[c]['gameduration'] = str(newList[c]['gameduration'])
        newList[c]['wins'] = str(newList[c]['wins'])
        newList[c]['losses'] = str(newList[c]['losses'])
        newList[c]['qntd'] = str(newList[c]['qntd'])
        
        newList[c]['winrate'] = str(newList[c]['winrate'])

    return(newList)


@shared_task
def matchv5_timeLine(matchid,requestplayer):
    MATCH_ID = matchid
    URL = f"https://americas.api.riotgames.com/lol/match/v5/matches/{MATCH_ID}/timeline?api_key={API_KEY}"
    response = requests.get(URL).json()
    
   # Catching the participants
    PARTICIPANTS = []
    participants = response['metadata']['participants']
    for puuid in participants:
        try:
            PARTICIPANTS.append(playerObject.objects.filter(puuid=puuid).get())
        except Exception as er:
            raise(er)
    ################################################################################################

    # Catchig the numbers of frames
    EVENTS_ARRAY = []

    for v in range(1,len(response['info']['frames'])):
        timeStamp = response['info']['frames'][v]['timestamp']
        TIME = math.floor(timeStamp/(1000*60))
        
        # Catching events
        for r in range(0,len(response['info']['frames'][v]['events'])): 
                # SKILL LEVEL UP
                if response['info']['frames'][v]['events'][r]['type'] == "SKILL_LEVEL_UP":
                    PARTICIPANT_ID = int(response['info']['frames'][v]['events'][r]['participantId']) - 1
                    SKILL = response['info']['frames'][v]['events'][r]['skillSlot']
                    if SKILL == 1:
                        SKILL_SLOT = "Q"
                    elif SKILL == 2:
                        SKILL_SLOT = "W"
                    elif SKILL == 3:
                        SKILL_SLOT= "E"
                    elif SKILL == 4:
                        SKILL_SLOT = "R"
                    else:
                        SKILL_SLOT = "Error_404_CODE_SKILL_NOT_FOUND"
                    
                    EVENT = "SKILL_LEVEL_UP"
                    x = {
                        "participantId": PARTICIPANTS[PARTICIPANT_ID].name,
                        "skillSlot": SKILL_SLOT,
                        "event": EVENT,
                        "time": str(TIME)
                    }
                    EVENTS_ARRAY.append(x)

                # ITEM PURCHASED
                if response['info']['frames'][v]['events'][r]['type'] == "ITEM_PURCHASED":
                    
                    PARTICIPANT_ID = int(response['info']['frames'][v]['events'][r]['participantId']) - 1

                    ITEM_ID = response['info']['frames'][v]['events'][r]['itemId']
                    PARTICIPANT_ID = int(response['info']['frames'][v]['events'][r]['participantId']) - 1
                    EVENT = "ITEM_PURCHASED"
                    x = {
                        "participantId": PARTICIPANTS[PARTICIPANT_ID].name,
                        "itemId": str(ITEM_ID),
                        "event": EVENT,
                        "time": str(TIME)
                    }
                    EVENTS_ARRAY.append(x)
                   
                
                if len(EVENTS_ARRAY) == 0:
                    continue
                                   
    match = matchObject.objects.filter(matchId=MATCH_ID).get()
    newMatchTimeLine = matchTimeLineObject()
    newMatchTimeLine.allEvents = EVENTS_ARRAY
    newMatchTimeLine.match = match
    newMatchTimeLine.save()

###################################################################################
# FN TO GET CATEGORY OF GAMES BASED IN THE RIOT API OFICIAL DOCUMENTATION ~ESPECIAL GAMEMODES NOT INCLUDED~
def getCategory(queueid):
    #REFERENCE LINK
    #https://static.developer.riotgames.com/docs/lol/queues.json
    """
    420 = 5v5 Ranked Solo

    400 = 5v5 Normal Alternado

    430 = 5v5 Normal Às cegas

    450 = 5v5 ARAM

    440 = 5v5 Ranked Flex

    830 = Coop vs AI Introdução

    840 = Coop vs AI Iniciante

    850 = Coop vs AI Intermediário

    900 = ARURF

    700 = Clash
    """
    category = ""
    if queueid == 420:
        category = "Ranked Solo"
        return category

    elif queueid == 400:
        category = "Normal Alternado"
        return category

    elif queueid == 430:
        category = "Normal Às cegas"
        return category

    elif queueid == 450:
        category = "ARAM"
        return category

    elif queueid == 440:
        category = "Ranked Flex"
        return category

    elif queueid == 830:
        category = "Coop vs AI Introdução"
        return category
    
    elif queueid == 840:
        category = "Coop vs AI Iniciante"
        return category

    elif queueid == 850:
        category = "Coop vs AI Intermediário"
        return category

    elif queueid == 900:
        category = "ARURF"
        return category

    elif queueid == 700:
        category = "Clash"
        return category
    else:
        category = "?"
        return category

@shared_task
def matchv5_info(MATCH,NAME):
    
    # GETTING INFO OVER THE MATCHS
    try:
        matchObject.objects.filter(matchId=MATCH).get()
        print('Match já existente no bd')
    except:
        match_v5_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{MATCH}?api_key={API_KEY}"
        response = requests.get(match_v5_url).json()
        
        matchv5_timeLine.delay(MATCH,NAME)
        # ID
        MATCH_ID = MATCH
        # TIME STAMPS
        CATEGORY = getCategory(response['info']['queueId'])
        GAME_START = response['info']['gameStartTimestamp']
        GAME_DURATION = response['info']['gameDuration']
        GAME_ENDING = response['info']['gameEndTimestamp']

        # PARTICIPANTS
        PARTICIPANTS = response['info']['participants']
        NEW_LIST_PARTICIPANTS = []
        for k in range(0,len(PARTICIPANTS)):

            #SUMMONER
            SUMMONER_PUUID = PARTICIPANTS[k]['puuid']
            SUMMONER_ID = PARTICIPANTS[k]['summonerId']
            PROFILE_ICON = PARTICIPANTS[k]['profileIcon']
            SUMMONER_LEVEL = PARTICIPANTS[k]['summonerLevel']
            SUMMONER_NAME = PARTICIPANTS[k]['summonerName']
            try:
                playerObject.objects.update_or_create(puuid=SUMMONER_PUUID,
                                                     defaults={
                                                        'puuid':SUMMONER_PUUID,
                                                        'summonerid':SUMMONER_ID,
                                                        'name':SUMMONER_NAME.lower(),
                                                        'icon':PROFILE_ICON,
                                                        'level':SUMMONER_LEVEL,})
            except Exception as er:
                print(SUMMONER_NAME)
                pass
                
            #########################################################

            # CHAMPION E ROLE
            CHAMPION = PARTICIPANTS[k]['championName']
            CHAMPION_LEVEL = json.dumps(PARTICIPANTS[k]['champLevel'])
            ROLE = PARTICIPANTS[k]['teamPosition']
            if ROLE == "UTILITY":
                ROLE = "SUPPORT"
            

            # RUNES
            """
            5001 Scaling Health (15-90 HP, lvls 1-18)
            5002 Armor (5 Armor)
            5003 Magic Resist (6 MR)
            5005 Attack Speed (9% Attack Speed)
            5007 Scaling Cooldown Reduction (1-10% CDR, lvls 1-18)
            5008 Adaptive Force (6 AD or 10 AP)
            """
            # STATS_RUNES                         
            STATS_RUNES_DEFENSE = json.dumps(PARTICIPANTS[k]['perks']['statPerks']['defense']) 
            STATS_RUNES_FLEX = json.dumps(PARTICIPANTS[k]['perks']['statPerks']['flex'])
            STATS_RUNES_OFFENSE = json.dumps(PARTICIPANTS[k]['perks']['statPerks']['offense'])

            # PRINCIPAL RUNES
            PRINCIPAL_RUNE_STYLE = json.dumps(PARTICIPANTS[k]['perks']['styles'][0]['style'])
            FIRST_PRINCIPAL_RUNE = json.dumps(PARTICIPANTS[k]['perks']['styles'][0]['selections'][0]['perk'])
            SECOND_PRINCIPAL_RUNE = json.dumps(PARTICIPANTS[k]['perks']['styles'][0]['selections'][1]['perk'])
            THIRD_PRINCIPAL_RUNE = json.dumps(PARTICIPANTS[k]['perks']['styles'][0]['selections'][2]['perk'])
            FOURTH_PRINCIPAL_RUNE = json.dumps(PARTICIPANTS[k]['perks']['styles'][0]['selections'][3]['perk'])

            # SECONDARY RUNES
            SECONDARY_RUNE_STYLE = json.dumps(PARTICIPANTS[k]['perks']['styles'][1]['style'])
            FIRST_SECONDARY_RUNE = json.dumps(PARTICIPANTS[k]['perks']['styles'][1]['selections'][0]['perk'])
            # Haha :)
            SECOND_SECONDARY_RUNE = json.dumps(PARTICIPANTS[k]['perks']['styles'][1]['selections'][1]['perk'])

            # SETTING RUNES DICT
            PRINCIPAL_RUNES = {
                "principalRuneStyle":PRINCIPAL_RUNE_STYLE,
                "1PrincipalRune":FIRST_PRINCIPAL_RUNE,
                "2PrincipalRune":SECOND_PRINCIPAL_RUNE,
                "3PrincipalRune":THIRD_PRINCIPAL_RUNE,
                "4PrincipalRune":FOURTH_PRINCIPAL_RUNE
            }
            SECONDARY_RUNES = {
                "secondaryRuneStyle":SECONDARY_RUNE_STYLE,
                "1SecondaryRune":FIRST_SECONDARY_RUNE,
                "2SecondaryRune":SECOND_SECONDARY_RUNE,
            }
            STATS_RUNES = {
                "statRuneAttack":STATS_RUNES_OFFENSE,
                "statRuneDefense":STATS_RUNES_DEFENSE,
                "statRuneFlex":STATS_RUNES_FLEX,
            }
            RUNES = {
                "principalRunes":PRINCIPAL_RUNES,
                "secondaryRunes":SECONDARY_RUNES,
                "statsRunes":STATS_RUNES
            }
            
            ##############################################################################################################
            # KDA
            ASSISTS = PARTICIPANTS[k]['assists']
            DEATHS = PARTICIPANTS[k]['deaths']
            KILLS = PARTICIPANTS[k]['kills']
            if DEATHS == 0:
                KDA = KILLS + ASSISTS
            else:
                KDA = round((KILLS + ASSISTS) / DEATHS, 2)
            # DMG,GOLD,ITEMS,WARDS
            TOTAL_CS = json.dumps(PARTICIPANTS[k]['totalMinionsKilled'] + PARTICIPANTS[k]['neutralMinionsKilled'])
            TOTAL_DMG = json.dumps(PARTICIPANTS[k]['totalDamageDealtToChampions'])
            WARDS = json.dumps(PARTICIPANTS[k]['wardsPlaced'])
            GOLD_EARNED = json.dumps(PARTICIPANTS[k]['goldEarned'])
            ITEM_0 = json.dumps(PARTICIPANTS[k]['item0'])
            ITEM_1 = json.dumps(PARTICIPANTS[k]['item1'])
            ITEM_2 = json.dumps(PARTICIPANTS[k]['item2'])
            ITEM_3 = json.dumps(PARTICIPANTS[k]['item3'])
            ITEM_4 = json.dumps(PARTICIPANTS[k]['item4'])
            ITEM_5 = json.dumps(PARTICIPANTS[k]['item5'])
            ITEM_6 = json.dumps(PARTICIPANTS[k]['item6'])

            # WIN THE MATCH? = TRUE OR FALSE
            WIN = json.dumps(PARTICIPANTS[k]['win'])

            PARTICIPANT = {
                "puuid":SUMMONER_PUUID,
                "summonerName":SUMMONER_NAME,
                "champion":CHAMPION,
                "championLevel":CHAMPION_LEVEL,
                "role":ROLE,
                "cs":TOTAL_CS,
                "runes":RUNES,
                "assists":json.dumps(ASSISTS),
                "deaths":json.dumps(DEATHS),
                "kills":json.dumps(KILLS),
                "kda":json.dumps(KDA),
                "totalDmg":TOTAL_DMG,
                "wards":WARDS,
                "goldEarned":GOLD_EARNED,
                "item0":ITEM_0,
                "item1":ITEM_1,
                "item2":ITEM_2,
                "item3":ITEM_3,
                "item4":ITEM_4,
                "item5":ITEM_5,
                "item6":ITEM_6,
                "win":WIN
            }
            NEW_LIST_PARTICIPANTS.append(PARTICIPANT)

        # TEAMS
        TEAMS = response['info']['teams']
        NEW_LIST_TEAMS = []
        for l in range(0,len(TEAMS)):
            # BAN LIST
            BANS_LIST = TEAMS[l]['bans']
            BANS = []
            for m in range(0,len(BANS_LIST)):
                CHAMPION = {
                    "championId":json.dumps(BANS_LIST[m]['championId'])
                }
                BANS.append(CHAMPION)

            # OBJECTIVES
            OBJECTIVES = TEAMS[l]['objectives']
            # ~
            BARON = json.dumps(OBJECTIVES['baron']['kills'])
            DRAGON = json.dumps(OBJECTIVES['dragon']['kills'])
            RIFTHERALD = json.dumps(OBJECTIVES['riftHerald']['kills'])
            KILLS = json.dumps(OBJECTIVES['champion']['kills'])
            INHIBITOR = json.dumps(OBJECTIVES['inhibitor']['kills'])
            TOWER = json.dumps(OBJECTIVES['tower']['kills'])

            # W = T OR F
            WIN = json.dumps(TEAMS[l]['win'])
            # BANS RETURN A LIST OF BANNED CHAMPION IDS
            TEAM = {
                "win":WIN,
                "bans":BANS,
                "barons":BARON,
                "dragons":DRAGON,
                "riftheralds":RIFTHERALD,
                "kills":KILLS,
                "inhibitor":INHIBITOR,
                "towers":TOWER
            }
            NEW_LIST_TEAMS.append(TEAM)

        # saving a new match in the database
        newObjectMatch = matchObject(matchId=MATCH_ID)
        newObjectMatch.gameStart = GAME_START
        newObjectMatch.category = CATEGORY
        newObjectMatch.gameEnding = GAME_ENDING
        newObjectMatch.gameDuration = GAME_DURATION
        newObjectMatch.participants = NEW_LIST_PARTICIPANTS
        newObjectMatch.teams = NEW_LIST_TEAMS
        newObjectMatch.save()
     
    ##############################################################

@shared_task
def match_v5(PUUID,NAME):
    # GETTING LAST 10 MATCHS
    MATCH_V5 = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{PUUID}/ids?start=0&count={PLAYER_MATCH_COUNT}&api_key={API_KEY}"
    response = requests.get(MATCH_V5).json()
    MATCH_LIST = []
    for match in response:
        MATCH_LIST.append(match)
        matchv5_info.delay(match,NAME)
    return MATCH_LIST
    ##############################################################

@shared_task
def league_v4(ID):
    # GETTING RANKED SOLO LEAGUE INFO
    LEAGUE_V4 = "https://br1.api.riotgames.com/lol/league/v4/entries/by-summoner/" + ID + \
        "?api_key=" + API_KEY
    response = requests.get(LEAGUE_V4).json()
    QUEUES_INFO = []
    for x in range(0,len(response)):
        print(str(len(response)))
        QUEUE = response[x]['queueType']
        if(QUEUE == "RANKED_TFT_PAIRS"):
           continue
        else:
            LEAGUE_ID = response[x]['leagueId']
            TIER = response[x]['tier']
            RANK = response[x]['rank']
            LEAGUE_POINTS = json.dumps(response[x]['leaguePoints'])
            WINS = json.dumps(response[x]['wins'])
            LOSSES = json.dumps(response[x]['losses'])

            # WIN RATIO
            totalmatchs = response[x]['wins'] + response[x]['losses']
            wins = response[x]['wins']

            WINRATE = json.dumps(round((wins / totalmatchs) * 100, 1))

            ########################

            RANKED_INFO = {
                "LEAGUE_ID": LEAGUE_ID,
                "QUEUE":QUEUE,
                "TIER":TIER,
                "RANK":RANK,
                "LEAGUE_POINTS":LEAGUE_POINTS,
                "WINS":WINS,
                "LOSSES":LOSSES,
                "WINRATE": WINRATE
            }
            QUEUES_INFO.append(RANKED_INFO)

    return QUEUES_INFO
    ##############################################################


@shared_task
def summoner_v4(player_name):
    # GETTING ID
    SUMMONER_V4 = "https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + player_name + \
          "?api_key=" + API_KEY

    response = requests.get(SUMMONER_V4).json()
    ID = response['id']
    QUEUES_INFO = league_v4.delay(ID)
    PUUID = response['puuid']
    NAME = response['name'].lower()
    MATCH_LIST = match_v5.delay(PUUID,NAME)
    ICON_ID = response['profileIconId']
    LEVEL = response['summonerLevel']

    ##############################################################
    tasks_not_concluded = False
    while tasks_not_concluded == False:
        if(QUEUES_INFO.ready() == True) and (MATCH_LIST.ready() == True):
            tasks_not_concluded = True
            PLAYER_CHAMPION_STATISTICS = player_champion_statistics.delay(PUUID)
        else:
            time.sleep(3)
        
    # saving a new player in the database
    with allow_join_result():
        RANKED_SOLO = QUEUES_INFO.get()
        MATCHS = MATCH_LIST.get()
        CHAMPIONSTATISTICS = PLAYER_CHAMPION_STATISTICS.get()
        
    obj,created = playerObject.objects.update_or_create(puuid=PUUID,
    defaults={
        'puuid':PUUID,
        'summonerid':ID,
        'name':NAME.lower(),
        'icon':ICON_ID,
        'level':LEVEL,
        'rankedSolo':RANKED_SOLO,
        'matchs':MATCHS,
        "championStatistics":CHAMPIONSTATISTICS
    })

    #############################################################
    