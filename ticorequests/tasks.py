from django.core import exceptions
from celery import shared_task
import json
import time
import math

from ticorequests import models
from utils import misc
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
            event_type = event['type']
            if event_type == "SKILL_LEVEL_UP" or event_type == "ITEM_PURCHASED":
                event_dict = {}
                partid = int(event['participantId']) - 1
                event_dict['participantId'] = partid
                event_dict['time'] = str(time)

                if event['type'] == "SKILL_LEVEL_UP":
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
                    event_dict['skillSlot'] = skill_slot
                    event_dict['event'] = "SKILL_LEVEL_UP"

                elif event['type'] == "ITEM_PURCHASED":
                    event_dict['itemId'] = str(event['itemId'])
                    event_dict['event'] = "ITEM_PURCHASED"

                events.append(event_dict)

    match = models.MatchObject.objects.get(match_id=match_id)
    newMatchTimeLine = models.MatchTimeLineObject()
    newMatchTimeLine.all_events = events
    newMatchTimeLine.match = match
    newMatchTimeLine.save()


@shared_task
def matchv5_info(match_id):
    # GETTING INFO OVER THE MATCHS
    try:
        models.MatchObject.objects.get(match_id=match_id)
        return print('Match já existente no bd')
    except exceptions.ObjectDoesNotExist:
        response = RiotLolService().get_matchv5(match_id).json()
        matchv5_timeLine.delay(match_id)
        participants = response['info']['participants']
        new_list_participants = []
        for participant in participants:
            summoner_puuid = participant['puuid']
            summoner_name = participant['summonerName']
            try:
                models.PlayerObject.objects.update_or_create(puuid=summoner_puuid,
                                                     defaults={
                                                        'puuid':summoner_puuid,
                                                        'summoner_id':participant['summonerId'],
                                                        'name':summoner_name.lower(),
                                                        'icon':participant['profileIcon'],
                                                        'level':participant['summonerLevel'],})
            except Exception as er:
                print(f"{summoner_name} raised {str(er)}")
                pass
                
            # STATS_RUNES                         
            stats_runes_defense = json.dumps(participant['perks']['statPerks']['defense']) 
            stats_runes_flex = json.dumps(participant['perks']['statPerks']['flex'])
            stats_runes_offense = json.dumps(participant['perks']['statPerks']['offense'])

            # PRINCIPAL RUNES
            principal_rune_style = json.dumps(participant['perks']['styles'][0]['style'])
            first_principal_rune = json.dumps(participant['perks']['styles'][0]['selections'][0]['perk'])
            second_principal_rune = json.dumps(participant['perks']['styles'][0]['selections'][1]['perk'])
            third_principal_rune = json.dumps(participant['perks']['styles'][0]['selections'][2]['perk'])
            fourth_principal_rune = json.dumps(participant['perks']['styles'][0]['selections'][3]['perk'])

            # SECONDARY RUNES
            secondary_rune_style = json.dumps(participant['perks']['styles'][1]['style'])
            first_secondary_rune = json.dumps(participant['perks']['styles'][1]['selections'][0]['perk'])
            second_secondary_rune = json.dumps(participant['perks']['styles'][1]['selections'][1]['perk'])

           
            # kda kill death assists
            assists = participant['assists']
            deaths = participant['deaths']
            kills = participant['kills']

            role = participant['teamPosition']

            participant_payload = {
                "puuid":summoner_puuid,
                "summonerName":summoner_name,
                "champion":participant['championName'],
                "championLevel":json.dumps(participant['champLevel']),
                "role":role if role != "UTILITY" else "SUPPORT",
                "cs":json.dumps(participant['totalMinionsKilled'] + participant['neutralMinionsKilled']),
                "runes":{
                    "principalRunes":{
                        "principalRuneStyle":principal_rune_style,
                        "1PrincipalRune":first_principal_rune,
                        "2PrincipalRune":second_principal_rune,
                        "3PrincipalRune":third_principal_rune,
                        "4PrincipalRune":fourth_principal_rune
                        },
                    "secondaryRunes":{
                        "secondaryRuneStyle":secondary_rune_style,
                        "1SecondaryRune":first_secondary_rune,
                        "2SecondaryRune":second_secondary_rune,
                        },
                    "statsRunes": {
                        "statRuneAttack":stats_runes_offense,
                        "statRuneDefense":stats_runes_defense,
                        "statRuneFlex":stats_runes_flex,
                        }
                    },
                "assists":json.dumps(assists),
                "deaths":json.dumps(deaths),
                "kills":json.dumps(kills),
                "kda":json.dumps(kills + assists if deaths == 0 else round((kills + assists) / deaths, 2)),
                "totalDmg":json.dumps(participant['totalDamageDealtToChampions']),
                "wards":json.dumps(participant['wardsPlaced']),
                "goldEarned":json.dumps(participant['goldEarned']),
                "item0":json.dumps(participant['item0']),
                "item1":json.dumps(participant['item1']),
                "item2":json.dumps(participant['item2']),
                "item3":json.dumps(participant['item3']),
                "item4":json.dumps(participant['item4']),
                "item5":json.dumps(participant['item5']),
                "item6":json.dumps(participant['item6']),
                "win":json.dumps(participant['win'])
            }
            new_list_participants.append(participant_payload)

        # TEAMS
        new_list_teams = []
        for team in response['info']['teams']:
            # BAN LIST
            bans = []
            for ban in team['bans']:
                champion = {
                    "championId":json.dumps(ban['championId'])
                }
                bans.append(champion)

            # BANS RETURN A LIST OF BANNED CHAMPION IDS
            team_dict = {
                "win":json.dumps(team['win']),
                "bans":bans,
                "barons":json.dumps(team['objectives']['baron']['kills']),
                "dragons":json.dumps(team['objectives']['dragon']['kills']),
                "riftheralds":json.dumps(team['objectives']['riftHerald']['kills']),
                "kills":json.dumps(team['objectives']['champion']['kills']),
                "inhibitor":json.dumps(team['objectives']['inhibitor']['kills']),
                "towers":json.dumps(team['objectives']['tower']['kills'])
            }
            new_list_teams.append(team_dict)

        # saving a new match in the database
        newObjectMatch = models.MatchObject(match_id=match_id)
        newObjectMatch.game_start = response['info']['gameStartTimestamp']
        newObjectMatch.category = misc.get_game_category(response['info']['queueId'])
        newObjectMatch.game_ending = response['info']['gameEndTimestamp']
        newObjectMatch.game_duration = response['info']['gameDuration']
        newObjectMatch.participants = new_list_participants
        newObjectMatch.teams = new_list_teams
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

    