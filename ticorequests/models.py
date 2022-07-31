from django.conf import settings
from django.db import models

from integrations.services.ddragoncdn import DragonCdnService
from utils.player import PlayerUtil

class PlayerObject(models.Model):
	puuid = models.CharField(max_length=100)
	summoner_id = models.CharField(max_length=100)
	name = models.CharField(max_length=100)
	icon = models.CharField(max_length=100)
	level = models.CharField(max_length=100)
	ranked_solo = models.TextField()
	championStatistics = models.TextField()
	matchs = models.TextField()

	def get_solo_league_info(self):
		self.ranked_solo = PlayerUtil(self.name).get_solo_league_info()
		super(PlayerObject, self).save()

	def get_champion_statistics(self):
		self.championStatistics = PlayerUtil(self.name).get_champion_statistics()
		super(PlayerObject, self).save()


class ItemObject(models.Model):
	item_id = models.CharField(max_length=100)
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=100)
	image = models.CharField(max_length=100)
	value = models.CharField(max_length=100)
	
	def save(self, *args, **kwargs):
		self.image = DragonCdnService().get_item_img_url(self.image)
		super(RunesObject, self).save(*args, **kwargs)

class MatchObject(models.Model):
	match_id = models.CharField(max_length=100)
	category = models.CharField(max_length=100)
	game_start = models.CharField(max_length=100)
	game_ending = models.CharField(max_length=100)
	game_duration = models.CharField(max_length=100)
	participants = models.TextField()
	teams = models.TextField()

class MatchTimeLineObject(models.Model):
	match = models.ForeignKey(MatchObject,on_delete=models.CASCADE)
	all_events = models.TextField()

class RunesObject(models.Model):
	rune_id = models.CharField(max_length=50)
	key = models.CharField(max_length=100)
	icon = models.CharField(max_length=100)
	name = models.CharField(max_length=100)
	description = models.TextField()
 
	def save(self, *args, **kwargs):
			self.icon = f"{settings.RIOT_DRAGON_CANISBACK_CDN_URL}{self.icon}"
			super(RunesObject, self).save(*args, **kwargs)
 

 
    
    	