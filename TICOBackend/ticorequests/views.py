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


def error_invalid_params():
    error = {"error":"invalid params"}
    print(error)
    return Response(data=error,status=status.HTTP_400_BAD_REQUEST)

class requestPlayerView(APIView):
    @api_view(('POST',))
    def request_player(request):
        params = request.data
        if "name" in params:
            player_name = params['name']
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
                    time.sleep(3)
            
        else:
            return error_invalid_params()        
        

class playerViewSet(viewsets.ModelViewSet):
    queryset = playerObject.objects.all()
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
                "desc":runeobj.desc
            }
            return Response(data=rune_info,status=status.HTTP_200_OK)
            
        elif "runes" in params:
            runes = params['runes']
            RUNES = []
            for rune in runes:
                rune_id = rune['id']
                runeobj = runesObject.objects.get(runeId=rune_id)
                rune_info = {
                "name":runeobj.name,
                "icon":runeobj.icon,
                "desc":runeobj.desc
                }
                RUNES.append(rune_info)
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
            if days > 1:
                x = time.seconds / 86400
                if x > 0.5:
                    timeAgo = str(days + 1) + " days ago"
                elif x < 0.5:
                    timeAgo = str(days) + " days ago"
            else:
                minutes = time.seconds / 60
                print(minutes)
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
            