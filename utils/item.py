from ticorequests.models import ItemObject
from integrations.services.ddragoncdn import DragonCdnService

class ItemUtils:
    def __init__(self,item_id):
        self.item_id = item_id
    
    def save_item(self,item_id,name_item,description_item,image_id,value_item):
        item_obj, created = ItemObject.objects.update_or_create(
                    item_id=item_id,
                    name=name_item,
                    description=description_item,
                    image=image_id,
                    value=value_item
                    )
        return item_obj

    def get_item_obj(self):
        return ItemObject.objects.get(item_id=self.item_id)

    def get_item_json(self):
        item = self.get_item_json()
        return {
            "name":item.name,
            "description":item.description,
            "image":item.image,
            "value":item.value
        }
    
    def update_items(self):
        items_data = DragonCdnService().get_items_info().json()["data"]
        for item_id in items_data:
            name_item = items_data[item_id]['name']
            description_item = items_data[item_id]['description']
            image_id = items_data[item_id]['image']['full']
            value_item = items_data[item_id]['gold']['total']

            self.save_item(item_id,
                            name_item,
                            description_item,
                            image_id,
                            value_item)
        