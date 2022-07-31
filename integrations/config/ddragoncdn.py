from django.conf import settings
import requests

class DragonCdnConfig:
    def __init__(self):
        self.dragon_cdn_url = settings.RIOT_DRAGON_CDN_URL
        self.dragon_version = self.get_dragon_version()
        self.dragon_language = "pt_BR"
    
    def get_dragon_version(self):
        url = f"{self.dragon_cdn_url}/api/versions.json"
        return requests.get(url).json()[0]