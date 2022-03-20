from pyexpat import model
from django.db import models

class playerObject(models.Model):
	puuid = models.CharField(max_length=100)
	summonerid = models.CharField(max_length=100)
	name = models.CharField(max_length=100)
	icon = models.CharField(max_length=100)
	level = models.CharField(max_length=100)
	rankedSolo = models.TextField()
	championStatistics = models.TextField()
	matchs = models.TextField()

class itemObject(models.Model):
    itemId = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

class matchObject(models.Model):
	matchId = models.CharField(max_length=100)
	category = models.CharField(max_length=100)
	gameStart = models.CharField(max_length=100)
	gameEnding = models.CharField(max_length=100)
	gameDuration = models.CharField(max_length=100)
	participants = models.TextField()
	teams = models.TextField()

class matchTimeLineObject(models.Model):
	match = models.ForeignKey(matchObject,on_delete=models.CASCADE)
	allEvents = models.TextField()

class runesObject(models.Model):
    
	runeId = models.CharField(max_length=50)
	key = models.CharField(max_length=100)
	icon = models.CharField(max_length=100)
	name = models.CharField(max_length=100)
	description = models.TextField()
 
	def save(self, *args, **kwargs):
			self.icon = f"https://ddragon.canisback.com/img/{self.icon}"
			super(runesObject, self).save(*args, **kwargs)
 

 
    
    	