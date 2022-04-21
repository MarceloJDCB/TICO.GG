from django.contrib import admin
from .models import playerObject,matchObject,runesObject,matchTimeLineObject,itemObject

admin.site.register(playerObject)
admin.site.register(matchObject)
admin.site.register(matchTimeLineObject)
admin.site.register(runesObject)
admin.site.register(itemObject)


