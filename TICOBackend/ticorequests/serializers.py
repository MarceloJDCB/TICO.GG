from rest_framework import serializers, exceptions
from .models import playerObject,matchObject

class playerSerializer(serializers.ModelSerializer):
	class Meta:
		model = playerObject
		fields ='__all__'

class matchSerializer(serializers.ModelSerializer):
	class Meta:
		model = matchObject
		fields ='__all__'

