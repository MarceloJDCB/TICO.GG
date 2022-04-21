from django.http import StreamingHttpResponse
from django.shortcuts import render
from rest_framework import viewsets, status
from .serializers import playerSerializer,matchSerializer
from .models import matchTimeLineObject, playerObject, runesObject,matchObject,itemObject
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from pytz import timezone
import time
from .tasks import summoner_v4
from .dictToJson import dictToJson
from datetime import datetime,timedelta
from .checkConnection import checkConnection
from .getMatch import get_match
from .getPlayerMatch import player_match
from .randomChampion import gen_champion
# Delete this and configure what you want
from .itemsService import update_items
from .runesService import update_runes

def index(response):
    print(gen_champion())
    return render(response,"ticorequests/index.html")

def matchs_unranked(response,summoner):
    matchs_list = dictToJson(playerObject.objects.filter(puuid=summoner).get().matchs)
    matchs = []
    
    for match in matchs_list:
        match_info = get_match(match)
        player_info_in_match = player_match(match,summoner)['participant']
        
        kills = player_info_in_match['kills']
        deaths = player_info_in_match['deaths']
        assists = player_info_in_match['assists']
        kda = f"{kills}/{deaths}/{assists}"
        match_info = {
            "id":match_info['gameEnding'],
            "category":match_info['category'],
            "timeAgo":match_info['timeAgo'],
            "gameDuration":match_info['gameDuration'],
            "matchId":match_info['matchId'],
            "champion":player_info_in_match['champion'],
            "kda":kda,
            "win":player_info_in_match['win']
            
        }
        matchs.append(match_info)
        
    #matchs = sorted(matchs, key = lambda i: i['id'])  
    matchs = {"matchs":matchs}
    return render(response,"ticorequests/matchs.html", matchs)

def matchs(response,summoner):
    matchs_list = dictToJson(playerObject.objects.filter(puuid=summoner).get().matchs)
    matchs = []
    
    for match in matchs_list:
        match_info = get_match(match)
        player_info_in_match = player_match(match,summoner)['participant']
        
        kills = player_info_in_match['kills']
        deaths = player_info_in_match['deaths']
        assists = player_info_in_match['assists']
        kda = f"{kills}/{deaths}/{assists}"
        if match_info['category'] == "Ranked Solo":
            match_info = {
                "id":match_info['gameEnding'],
                "category":match_info['category'],
                "timeAgo":match_info['timeAgo'],
                "gameDuration":match_info['gameDuration'],
                "matchId":match_info['matchId'],
                "champion":player_info_in_match['champion'],
                "kda":kda,
                "win":player_info_in_match['win']
                
            }
            matchs.append(match_info)
        else: continue
        
    if matchs == []:
        
        for match in matchs_list:
            match_info = get_match(match)
            player_info_in_match = player_match(match,summoner)['participant']
            
            kills = player_info_in_match['kills']
            deaths = player_info_in_match['deaths']
            assists = player_info_in_match['assists']
            kda = f"{kills}/{deaths}/{assists}"
            match_info = {
                "id":match_info['gameEnding'],
                "category":match_info['category'],
                "timeAgo":match_info['timeAgo'],
                "gameDuration":match_info['gameDuration'],
                "matchId":match_info['matchId'],
                "champion":player_info_in_match['champion'],
                "kda":kda,
                "win":player_info_in_match['win']}
            matchs.append(match_info)
            
      
    matchs = {"matchs":matchs}
    return render(response,"ticorequests/matchs.html", matchs)

def summoner(response,summoner):
    summoner = summoner.lower()
    
    if checkConnection(summoner):
        summoner_task = summoner_v4.delay(summoner)
        
        tasks_not_concluded = False
        while tasks_not_concluded == False:
            if summoner_task.ready() == True:
                player = playerObject.objects.filter(name=summoner).get()
                rankedsolo = (dictToJson(player.rankedSolo))
                champions_statistics = dictToJson(player.championStatistics)
                champion_qtd = 0
                champion_name = ""
                for champion in champions_statistics:
                    ch_qtd = int(champion['qntd'])
                    if ch_qtd > champion_qtd:
                        champion_qtd = ch_qtd
                        champion_name = champion['champion']
                    else:
                        continue
                ranked_solo_info = ""
                for itens in rankedsolo:
                    if itens['QUEUE'] == 'RANKED_SOLO_5x5':
                        tier = itens['TIER']
                        pdl = itens['LEAGUE_POINTS']
                        wins = itens['WINS']
                        losses = itens['LOSSES']
                        winrate = itens['WINRATE']
                        w_l = f"{wins}W {losses} L"
                        ranked_solo_info = {"tier":tier, "pdl":pdl, "wl":w_l,"winrate":winrate}
                if ranked_solo_info == "":
                    
                    champion_name = gen_champion()
                    player_info = {
                        "player":player,
                        "champion_name":champion_name
                    }
                    print(player_info)
                    return render(response,"ticorequests/summonerunranked.html", player_info)
                    
                        
                else:
                    if champion_name == "":
                        champion_name = gen_champion()
                    player_info = {
                        "player":player,
                        "champion_name":champion_name
                    }
                    print(champion_name)
                    player_info = dict(player_info,**ranked_solo_info)
                    return render(response,"ticorequests/summoner.html", player_info)
            else:
                time.sleep(1)
                continue
            
    else:
        return render(response,"ticorequests/error_riot.html")
    
    
    
    
    

    

def test(request):
    rx = playerObject.objects.filter(name="rxrxatiradorrxrx")
    
    print(rx)
    return Response(data=rx)


def error_invalid_params():
    error = {"error":"invalid params"}
    print(error)
    return Response(data=error,status=status.HTTP_400_BAD_REQUEST)


class requestPlayerView(APIView):
    @api_view(('POST',))
    def request_player(request):
        params = request.data
        if "name" in params:
            player_name = params['name'].lower()
            if checkConnection(player_name):
                summoner_task = summoner_v4.delay(player_name)
                
                tasks_not_concluded = False
                while tasks_not_concluded == False:
                    if summoner_task.ready() == True:
                        tasks_not_concluded = True
                        requested_player = playerObject.objects.get(name=player_name)
                        # LOAD THE DATA FROM THE RANKED
                        RANKED_TEXT =  requested_player.rankedSolo
                        data_ranked = dictToJson(RANKED_TEXT)
                        ##################################################################
                        # LOAD THE DATA FROM THE MATCHS
                        MATCH_TEXT =  requested_player.matchs
                        data_matchs = dictToJson(MATCH_TEXT)
                        ##################################################################
                        # LOAD THE STATISTICS FROM THE CHAMPIONS
                        CHAMPIONS_TEXT = requested_player.championStatistics
                        data_champions = dictToJson(CHAMPIONS_TEXT)
                        ###################################################################
                        player_data = {
                            "puuid": requested_player.puuid,
                            "summonerid": requested_player.summonerid,
                            "name": requested_player.name,
                            "icon": requested_player.icon,
                            "level": requested_player.level,
                            "ranked": data_ranked,
                            "matchs": data_matchs,
                            "championStatistics": data_champions
                        }
                        return Response(player_data, status.HTTP_200_OK)
                    else:
                        render(request,"ticorequests/loading.html")
                        continue
                    
            else:
                error = {"error":"Connection to riot api was not successful"}
                return Response(data=error,status=status.HTTP_503_SERVICE_UNAVAILABLE)
            
        else:
            return error_invalid_params()        
        

class playerViewSet(viewsets.ModelViewSet):
    
    queryset = playerObject.objects.filter(name="grevzin")
    serializer_class = playerSerializer
   
class matchViewSet(viewsets.ModelViewSet):
    queryset = matchObject.objects.all()
    serializer_class = matchSerializer

class matchTimeLinePlayerView(APIView):
    @api_view(('POST',))
    def getTimeLine(request):
        params = request.data
        if "matchid" and "name" in params:
            match_id = params['matchid']
            player = params['name']
            match_object = matchObject.objects.get(matchId=match_id)
            matchtimeline = matchTimeLineObject.objects.get(match=match_object.id)
            # LOAD THE DATA FROM THE PARTICIPANTS
            MATCH_TIMELINE_TEXT = matchtimeline.allEvents
            data_timeline = dictToJson(MATCH_TIMELINE_TEXT)
            ##############################################
            Events_player = []
            for data in data_timeline:
                if data["participantId"] == player:
                    Events_player.append(data)
                else:
                    continue                               
            response = {
                "TimeLine":Events_player
            }
            return Response(response)            
        elif "matchid" in params:
            match_id = params['matchid']
            match_object = matchObject.objects.get(matchId=match_id)
            matchtimeline = matchTimeLineObject.objects.get(match=match_object.id)
            #LOAD THE DATA FROM THE PARTICIPANTS
            MATCH_TIMELINE_TEXT = matchtimeline.allEvents
            data_timeline = dictToJson(MATCH_TIMELINE_TEXT)
            ##############################################
            response = {
                "TimeLine":data_timeline
            }
            return Response(response)
        else:
            return error_invalid_params()

class itemView(APIView):
    @api_view(('POST',))
    def get_item(request):
        params = request.data
        if "id" in params:
            item_id = params['id']
            itemObj = itemObject.objects.get(itemId=item_id)
            item_info = {
                "name":itemObj.name,
                "description":itemObj.description,
                "image":itemObj.image,
                "value":itemObj.value
            }
            return Response(data=item_info,status=status.HTTP_200_OK)
        elif "items" in params:
            items = params['items']
            ITEMS = []
            for item in items:
                item_id = item['id']
                itemObj = itemObject.objects.get(itemId=item_id)
                item_info = {
                "name":itemObj.name,
                "description":itemObj.description,
                "image":itemObj.image,
                "value":itemObj.value
                }
                ITEMS.append(item_info)
            return Response(data=ITEMS,status=status.HTTP_200_OK)
        else:
            return error_invalid_params()
            

class runeView(APIView):
    @api_view(('POST',))
    def get_rune(request):
        params = request.data
        if "id" in params:
            rune_id = params['id']
            runeobj = runesObject.objects.get(runeId=rune_id)
         
            rune_info = {
                "name":runeobj.name,
                "icon":runeobj.icon,
                "desc":runeobj.description
            }
            return Response(data=rune_info,status=status.HTTP_200_OK)
            
        elif "runes" in params:
            runes = params['runes']
            RUNES = []
            for rune in runes:
                rune_id = rune['id']
                try:
                    runeobj = runesObject.objects.get(runeId=rune_id)
                    rune_info = {
                    "name":runeobj.name,
                    "icon":runeobj.icon,
                    "desc":runeobj.description
                    }
                    RUNES.append(rune_info)
                except:
                    error = {"error":"rune not found in the database"}
                    RUNES.append(error)
            return Response(data=RUNES,status=status.HTTP_200_OK)
        else:
            return error_invalid_params()
        
        

class matchView(APIView):
    @api_view(('POST',))
    def get_match(request):
        params = request.data
        if "matchid" and "player" in params:
            match_id = params['matchid']
            playerpuuid = params['player']
            match = matchObject.objects.get(matchId=match_id)
            # LOAD THE DATA FROM THE PARTICIPANT
            PARTICIPANTS_TEXT =  match.participants
            data_participants = dictToJson(PARTICIPANTS_TEXT)
            participant = ""
            for player in data_participants:
                if player['puuid'] == playerpuuid:
                    participant = player
                else:
                    continue                   
            ##################################################################
    
            MATCH_DATA = {
                "participant":participant,
            }
            return Response(MATCH_DATA)
        
        
        elif "matchid" in params:
            match_id = params['matchid']
            match = matchObject.objects.get(matchId=match_id)

            # CONVERTING TIMESTAMP TO NORMAL DATE
            # GAME DURATION
            duration = timedelta(seconds=int(match.gameDuration))
            sduration = str(duration)
            gameDuration = sduration[2:len(sduration)]

            timeStamp = float(match.gameEnding)
            gameEnding = datetime.fromtimestamp(timeStamp/1000, tz = timezone("Brazil/East"))
            #DAYS AGO
            EndingDate = datetime(gameEnding.year, gameEnding.month, gameEnding.day, gameEnding.hour, 0, 0)
            #HOURS AGO
            time = (datetime.now() - EndingDate)
            
            days = time.days
            if days > 0:
                x = time.seconds / 86400
                if x > 0.5:
                    timeAgo = str(days + 1) + " days ago"
                elif x < 0.5:
                    timeAgo = str(days) + " days ago"
            else:
                minutes = time.seconds / 60
                if minutes < 60:
                    timeAgo = str(minutes) + "minutes ago"
                elif minutes > 60:
                    timeAgo = str(round(minutes / 60)) + " hours ago"
    

            # LOAD THE DATA FROM THE PARTICIPANTS
            PARTICIPANTS_TEXT =  match.participants
            data_participants = dictToJson(PARTICIPANTS_TEXT)
            ##################################################################

            # LOAD THE DATA FROM THE TEAMS
            TEAMS_TEXT =  match.teams   
            data_teams = dictToJson(TEAMS_TEXT)
            ##################################################################

            MATCH_DATA = {
                "matchId":match.matchId,
                "category":match.category,
                "gameDuration":gameDuration,
                "timeAgo":timeAgo,
                "participants":data_participants,
                "teams":data_teams
            }
            return Response(MATCH_DATA)
        else:
            return error_invalid_params()
            