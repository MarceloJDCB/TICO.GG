from django.conf import settings

class RiotApiConfig:
    def __init__(self):
        self.america_base_api_link = settings.AMERICAS_RIOT_API_URL 
        self.br1_base_api_link = settings.BR1_RIOT_API_URL
        self.riot_api_token = settings.RIOT_API_KEY