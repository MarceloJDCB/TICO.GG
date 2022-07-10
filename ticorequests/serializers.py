from rest_framework import serializers, exceptions
from . import models

class requestPlayerSerializer(serializers.Serializer):
	player_name = serializers.CharField(allow_null=False,required=True)

class RunesSerializer(serializers.Serializer):
	runes = serializers.JSONField()

class RuneSerializer(serializers.Serializer):
	rune_id = serializers.IntegerField(allow_null=False,required=True)

class ItemsSerializer(serializers.Serializer):
	items = serializers.JSONField()

class ItemSerializer(serializers.Serializer):
	item_id = serializers.IntegerField(allow_null=False,required=True)
	
class RequestPlayerSerializer(serializers.Serializer):
	player_name = serializers.CharField(allow_null=False,required=True)

class MatchTimeLineSerializer(serializers.Serializer):
	match_id = serializers.CharField(allow_null=False,required=True)

class MatchTimeLinePlayerSerializer(serializers.Serializer):
	match_id = serializers.CharField(allow_null=False,required=True)
	player_name = serializers.CharField(allow_null=False,required=True)

class MatchSerializer(serializers.Serializer):
	match_id = serializers.CharField(allow_null=False,required=True)

class MatchSpecificPlayerSerializer(serializers.Serializer):
	match_id = serializers.CharField(allow_null=False,required=True)
	player_puuid = serializers.CharField(allow_null=False,required=True)

class playerSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.PlayerObject
		fields ='__all__'

class matchSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.MatchObject
		fields ='__all__'

