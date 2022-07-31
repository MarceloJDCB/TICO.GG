from django.contrib import admin
from . import models

admin.site.register(models.PlayerObject)
admin.site.register(models.MatchObject)
admin.site.register(models.MatchTimeLineObject)
admin.site.register(models.RunesObject)
admin.site.register(models.ItemObject)


