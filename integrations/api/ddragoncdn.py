from integrations.config.ddragoncdn import DragonCdnConfig
from rest_framework.response import Response
from rest_framework import status
import requests

class DragonCdnApi:
    def __init__(self):
        self.dragon_config = DragonCdnConfig()
        
    def get_runes_info(self):
        url = f"{self.dragon_config.dragon_cdn_url}/cdn/{self.dragon_config.dragon_version}/data/{self.dragon_config.dragon_language}/runesReforged.json"
        return self.dragon_request(url,'','GET')
    
    def get_items_info(self):
        url = f"{self.dragon_config.dragon_cdn_url}/cdn/{self.dragon_config.dragon_version}/data/{self.dragon_config.dragon_language}/item.json"
        return self.dragon_request(url,'','GET')

    def get_item_img_url(self,item_id):
        return f"{self.dragon_config.dragon_cdn_url}/cdn/{self.dragon_config.dragon_version}/img/item/{item_id}"
    
    def dragon_request(self,url,data,method):
        try:
            response = requests.request(
                method,
                url,
                data=data
            )
            if response.status_code != 200:
                return Response(data={"error":"Connection to dragon api was not successful"},status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as er:
            raise(er)

        return response
