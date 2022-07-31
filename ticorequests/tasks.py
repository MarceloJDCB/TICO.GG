from __future__ import absolute_import, unicode_literals
from django.core import exceptions
from celery import shared_task
import json
import time

import math
from . import models
from integrations.services.riotlolapi import RiotLolService

@shared_task
def matchv5_timeLine(match_id):
    response = RiotLolService().get_matchv5_timeline(match_id).json()
    participants = []
    participants_payload = response['metadata']['participants']
    for puuid in participants_payload:
        participants.append(models.PlayerObject.objects.get(puuid=puuid))

    # Catchig the numbers of frames
    events = []
    frames = response['info']['frames']
    for frame in frames:
        time_stamp = frame['timestamp']
        time = math.floor(time_stamp/(1000*60))
        
        # Catching events
        for event in frame['events']: 
                # SKILL LEVEL UP
                if event['type'] == "SKILL_LEVEL_UP":
                    participant_id = int(event['participantId']) - 1
                    skill = event['skillSlot']
                    if skill == 1:
                        skill_slot = "Q"
                    elif skill == 2:
                        skill_slot = "W"
                    elif skill == 3:
                        skill_slot= "E"
                    elif skill == 4:
                        skill_slot = "R"
                    else:
                        skill_slot = "Error_404_CODE_SKILL_NOT_FOUND"
                    
                    event_action = "SKILL_LEVEL_UP"
                    x = {
                        "participantId": participants[participant_id].name,
                        "skillSlot": skill_slot,
                        "event": event_action,
                        "time": str(time)
                    }
                    events.append(x)

                # ITEM PURCHASED
                if event['type'] == "ITEM_PURCHASED":
                    
                    participant_id = int(event['participantId']) - 1

                    item_id = event['itemId']
                    participant_id = int(event['participantId']) - 1
                    event_action = "ITEM_PURCHASED"
                    x = {
                        "participantId": participants[participant_id].name,
                        "itemId": str(item_id),
                        "event": event_action,
                        "time": str(time)
                    }
                    events.append(x)
                                   
    match = models.MatchObject.objects.get(match_id=match_id)
    newMatchTimeLine = models.MatchTimeLineObject()
    newMatchTimeLine.all_events = events
    newMatchTimeLine.match = match
    newMatchTimeLine.save()

############################################################################################################
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
def matchv5_info(match):
    
    # GETTING INFO OVER THE MATCHS
    try:
        models.MatchObject.objects.get(match_id=match)
        print('Match já existente no bd')
        return 0
    except exceptions.ObjectDoesNotExist:
        response = RiotLolService().get_matchv5(match).json()
        
        matchv5_timeLine.delay(match)
        # ID
        MATCH_ID = match
        # TIME STAMPS
        CATEGORY = getCategory(response['info']['queueId'])
        GAME_START = response['info']['gameStartTimestamp']
        GAME_DURATION = response['info']['gameDuration']
        GAME_ENDING = response['info']['gameEndTimestamp']

        # PARTICIPANTS
        PARTICIPANTS = response['info']['participants']
        new_list_participants = []
        for participant in PARTICIPANTS:

            #SUMMONER
            SUMMONER_PUUID = participant['puuid']
            SUMMONER_ID = participant['summonerId']
            PROFILE_ICON = participant['profileIcon']
            SUMMONER_LEVEL = participant['summonerLevel']
            SUMMONER_NAME = participant['summonerName']
            try:
                models.PlayerObject.objects.update_or_create(puuid=SUMMONER_PUUID,
                                                     defaults={
                                                        'puuid':SUMMONER_PUUID,
                                                        'summoner_id':SUMMONER_ID,
                                                        'name':SUMMONER_NAME.lower(),
                                                        'icon':PROFILE_ICON,
                                                        'level':SUMMONER_LEVEL,})
            except Exception as er:
                print(SUMMONER_NAME)
                pass
                
            # CHAMPION AND ROLE
            CHAMPION = participant['championName']
            CHAMPION_LEVEL = json.dumps(participant['champLevel'])
            ROLE = participant['teamPosition']
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
            STATS_RUNES_DEFENSE = json.dumps(participant['perks']['statPerks']['defense']) 
            STATS_RUNES_FLEX = json.dumps(participant['perks']['statPerks']['flex'])
            STATS_RUNES_OFFENSE = json.dumps(participant['perks']['statPerks']['offense'])

            # PRINCIPAL RUNES
            PRINCIPAL_RUNE_STYLE = json.dumps(participant['perks']['styles'][0]['style'])
            FIRST_PRINCIPAL_RUNE = json.dumps(participant['perks']['styles'][0]['selections'][0]['perk'])
            SECOND_PRINCIPAL_RUNE = json.dumps(participant['perks']['styles'][0]['selections'][1]['perk'])
            THIRD_PRINCIPAL_RUNE = json.dumps(participant['perks']['styles'][0]['selections'][2]['perk'])
            FOURTH_PRINCIPAL_RUNE = json.dumps(participant['perks']['styles'][0]['selections'][3]['perk'])

            # SECONDARY RUNES
            SECONDARY_RUNE_STYLE = json.dumps(participant['perks']['styles'][1]['style'])
            FIRST_SECONDARY_RUNE = json.dumps(participant['perks']['styles'][1]['selections'][0]['perk'])
            SECOND_SECONDARY_RUNE = json.dumps(participant['perks']['styles'][1]['selections'][1]['perk'])

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
            
            # KDA
            ASSISTS = participant['assists']
            DEATHS = participant['deaths']
            KILLS = participant['kills']
            if DEATHS == 0:
                KDA = KILLS + ASSISTS
            else:
                KDA = round((KILLS + ASSISTS) / DEATHS, 2)
            # DMG,GOLD,ITEMS,WARDS
            TOTAL_CS = json.dumps(participant['totalMinionsKilled'] + participant['neutralMinionsKilled'])
            TOTAL_DMG = json.dumps(participant['totalDamageDealtToChampions'])
            WARDS = json.dumps(participant['wardsPlaced'])
            GOLD_EARNED = json.dumps(participant['goldEarned'])
            ITEM_0 = json.dumps(participant['item0'])
            ITEM_1 = json.dumps(participant['item1'])
            ITEM_2 = json.dumps(participant['item2'])
            ITEM_3 = json.dumps(participant['item3'])
            ITEM_4 = json.dumps(participant['item4'])
            ITEM_5 = json.dumps(participant['item5'])
            ITEM_6 = json.dumps(participant['item6'])

            # WIN THE MATCH? = TRUE OR FALSE
            WIN = json.dumps(participant['win'])

            participant_payload = {
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
            new_list_participants.append(participant_payload)

        # TEAMS
        TEAMS = response['info']['teams']
        NEW_LIST_TEAMS = []
        for team in TEAMS:
            # BAN LIST
            BANS_LIST = team['bans']
            BANS = []
            for ban in BANS_LIST:
                CHAMPION = {
                    "championId":json.dumps(ban['championId'])
                }
                BANS.append(CHAMPION)

            # OBJECTIVES
            OBJECTIVES = team['objectives']
            # ~
            BARON = json.dumps(OBJECTIVES['baron']['kills'])
            DRAGON = json.dumps(OBJECTIVES['dragon']['kills'])
            RIFTHERALD = json.dumps(OBJECTIVES['riftHerald']['kills'])
            KILLS = json.dumps(OBJECTIVES['champion']['kills'])
            INHIBITOR = json.dumps(OBJECTIVES['inhibitor']['kills'])
            TOWER = json.dumps(OBJECTIVES['tower']['kills'])

            # W = T OR F
            WIN = json.dumps(team['win'])
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
        newObjectMatch = models.MatchObject(match_id=MATCH_ID)
        newObjectMatch.game_start = GAME_START
        newObjectMatch.category = CATEGORY
        newObjectMatch.game_ending = GAME_ENDING
        newObjectMatch.game_duration = GAME_DURATION
        newObjectMatch.participants = new_list_participants
        newObjectMatch.teams = NEW_LIST_TEAMS
        newObjectMatch.save()
     

@shared_task
def match_v5(player_id):
    player_obj = models.PlayerObject.objects.get(summoner_id=player_id)
    response = RiotLolService().get_matchv5_list(player_obj.puuid).json()
    match_list = []
    matchv5_info_tasks = []
    for match in response:
        match_list.append(match)
        matchv5_info_task = matchv5_info.delay(match)
        matchv5_info_tasks.append(matchv5_info_task)
    player_obj.matchs = match_list
    player_obj.save()

    while matchv5_info_tasks[-1].ready() == False:
        time.sleep(0.3)
    player_obj.get_champion_statistics()


@shared_task
def summoner_v4(player_name):
    # GETTING ID
    response = RiotLolService().get_summonnerv4(player_name).json()
    player_id = response['id']
    puuid = response['puuid']
    name = response['name'].lower()
    icon_id = response['profileIconId']
    player_level = response['summonerLevel']

    player_created,created = models.PlayerObject.objects.update_or_create(puuid=puuid,
                                                                    defaults={
                                                                    'puuid':puuid,
                                                                    'summoner_id':player_id,
                                                                    'name':name.lower(),
                                                                    'icon':icon_id,
                                                                    'level':player_level,})

    player_created.get_solo_league_info()
    match_v5.delay(player_id)

    