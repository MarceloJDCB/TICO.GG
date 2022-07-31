from rest_framework import viewsets, status
from .serializers import playerSerializer,matchSerializer
from . import models
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .tasks import summoner_v4
from datetime import datetime,timedelta
# Delete this and configure what you want
from ticorequests import serializers
from django.core import exceptions
from utils import match, player, item, rune

class TestView(APIView):
    @api_view(('GET',))
    def get_test(request):
        xxx = models.PlayerObject.objects.get(name='fã do takeshi')
        xxx.get_champion_statistics()
        print(xxx.championStatistics)
        return Response(data={"ok"})

class requestPlayerView(APIView):

    @api_view(('POST',))
    def request_player(request):
        params = request.data
        serializers.RequestPlayerSerializer(data=params).is_valid(raise_exception=True)
        player_name = params['player_name'].lower()
        summoner_task = summoner_v4.delay(player_name)
        return Response(data={"success"},status=status.HTTP_200_OK)
                
    @api_view(('POST',))
    def get_player(request):
        params = request.data
        serializers.RequestPlayerSerializer(data=params).is_valid(raise_exception=True)
        player_name = params['player_name'].lower()
        response = player.PlayerUtil(player_name).get_player_json()
        return Response(response, status.HTTP_200_OK)

class playerViewSet(viewsets.ModelViewSet):
    
    queryset = models.PlayerObject.objects.all()
    serializer_class = playerSerializer
   
class matchViewSet(viewsets.ModelViewSet):
    queryset = models.MatchObject.objects.all()
    serializer_class = matchSerializer

class matchTimeLinePlayerView(APIView):
    @api_view(('POST',))
    def get_time_line(request):
        params = request.data
        serializers.MatchTimeLineSerializer(data=params).is_valid(raise_exception=True)
        response = {
            "time_line":match.MatchTimelineUtils(params['match_id']).format_events_textfield()
        }
        return Response(response)

    @api_view(('POST',))
    def get_player_time_line(request):
        params = request.data
        serializers.MatchTimeLinePlayerSerializer(data=params).is_valid(raise_exception=True)
        response = {
            "time_line":match.MatchTimelineUtils(params['match_id']).get_player_timeline(params['player_name'])
        }
        return Response(response)        

class itemView(APIView):
    @api_view(('POST',))
    def get_item(request):
        params = request.data
        serializers.ItemSerializer(data=params).is_valid(raise_exception=True)
        item_info = item.ItemUtils(params['item_id']).get_item_json()
        return Response(data=item_info,status=status.HTTP_200_OK)

    def get_items(request):
        params = request.data
        serializers.ItemsSerializer(data=params).is_valid(raise_exception=True)
        items = params['items']
        items_payload = []
        for item_payload in items:
            item_info = item.ItemUtils(item_payload['id']).get_item_json()
            items_payload.append(item_info)
        return Response(data=items_payload,status=status.HTTP_200_OK)
            

class runeView(APIView):
    @api_view(('POST',))
    def get_rune(request):
        params = request.data
        serializers.RuneSerializer(data=params).is_valid(raise_exception=True)
        return Response(data=rune.RuneUtils(params['rune_id']).get_rune_json(),status=status.HTTP_200_OK)

    def get_runes(request):  
        params = request.data
        serializers.RunesSerializer(data=params).is_valid(raise_exception=True)
        runes = params['runes']
        runes_response = []
        for rune_payload in runes:
            try:
                runes_response.append(rune.RuneUtils(rune_payload['id']).get_rune_json())
            except exceptions.ObjectDoesNotExist:
                runes_response.append({"error":"rune not found in the database"})
            except Exception as er:
                raise(er)
        return Response(data=runes_response,status=status.HTTP_200_OK)
        

class matchView(APIView):
    @api_view(('POST',))
    def get_match(request):
        params = request.data
        serializers.MatchSerializer(data=params).is_valid(raise_exception=True)
        match_utils = match.MatchUtils(params['match_id'])
        response = match_utils.get_match_json()
        return Response(data={"response":response},status=status.HTTP_200_OK)
    
    def get_match_specific_player(request):
        params = request.data
        serializers.MatchSpecificPlayerSerializer(data=params).is_valid(raise_exception=True)
        match_utils = match.MatchUtils(params['match_id'])
        player_puuid = params['player']
        response = match_utils.get_specific_player_match(player_puuid)
        return Response(data={"response":response},status=status.HTTP_200_OK)
            