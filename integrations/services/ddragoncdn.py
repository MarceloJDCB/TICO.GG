from integrations.api.ddragoncdn import DragonCdnApi

class DragonCdnService:
    def __init__(self):
        self.dragon_api = DragonCdnApi()
    
    def get_runes_info(self):
        return self.dragon_api.get_runes_info()
    
    def get_items_info(self):
        return self.dragon_api.get_items_info()

    def get_item_img_url(self,item_id):
        return self.dragon_api.get_item_img_url(item_id)


    