from ticorequests.models import RunesObject
from integrations.services.ddragoncdn import DragonCdnService

class RuneUtils:
    def __init__(self,rune_id):
        self.rune_id = rune_id
    
    def get_rune_obj(self):
        return RunesObject.objects.get(rune_id=self.rune_id)

    def save_rune(rune_id,rune_key,rune_icon,rune_name,rune_desc):
        rune_obj, created = RunesObject.objects.update_or_create(
            rune_id=rune_id,
            key=rune_key,
            icon=rune_icon,
            name=rune_name,
            description=rune_desc
        )
        return rune_obj
    
    def get_rune_json(self):
        rune = self.get_rune_obj()
        return {
            "name":rune.name,
            "icon":rune.icon,
            "desc":rune.description
        }

    
    def update_runes(self):
        runes_json = DragonCdnService().get_runes_info().json()
        for rune_info in runes_json:
            self.save_rune(
                rune_info['id'],
                rune_info['key'],
                rune_info['icon'],
                rune_info['name'],
                '')
            
            slots = rune_info['slots']
            for slot in slots:
                runes_slot = slot['runes']
                for rune_slot_info in runes_slot:
                    self.save_rune(rune_slot_info['id'],
                                    rune_slot_info['key'],
                                    rune_slot_info['icon'],
                                    rune_slot_info['name'],
                                    rune_slot_info['longDesc'])
            