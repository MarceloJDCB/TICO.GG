import requests

from integrations.config.ddragoncdn import DragonCdnConfig
from integrations.models.riot import BaseApiCall

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
                data=data,
            )
            if response.status_code in [200,201]:
                BaseApiCall.objects.create(
                    api="DRAGON_CDN",
                    method=method,
                    url=url,
                    data=data,
                    success=True,
                    response_status_code=response.status_code,
                    response_data=response.json()
                )
            else:
                BaseApiCall.objects.create(
                    api="DRAGON_CDN",
                    method=method,
                    url=url,
                    data=data,
                    success=True,
                    response_status_code=response.status_code,
                    response_data=response.json()
                )
        except Exception as er:
            BaseApiCall.objects.create(
                    api="DRAGON_CDN",
                    method=method,
                    url=url,
                    data=data,
                    success=False,
                    response_status_code=response.status_code or None,
                    response_data=f"{er} / {response.json()}"
                )
        return response
