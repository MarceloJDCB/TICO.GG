import requests
from .models import itemObject

def update_items():
    # CREATING PARAMETERS TO GET THE ACTUAL VERSION OF DATA DRAGON AND LANGUAGE
    dragon_version_response = requests.get('https://ddragon.leagueoflegends.com/api/versions.json').json()
    actual_version = dragon_version_response[0]
    selected_language = "pt_BR"

    # GETTING INFO FOR THE RUNES
    info_items_response = requests.get(f'https://ddragon.leagueoflegends.com/cdn/{actual_version}/data/{selected_language}/item.json').json()
    data = info_items_response["data"]

    for item_id in data:
        # CATCHING INFORMATION FROM THE RESPONSE
        name_item = data[item_id]['name']
        description_item = data[item_id]['description']
        #image
        id = data[item_id]['image']['full']
        urlimage = f"http://ddragon.leagueoflegends.com/cdn/{actual_version}/img/item/{id}"
        
        #gold
        value_item = data[item_id]['gold']['total']

        try:
            obj, created = itemObject.objects.update_or_create(
                itemId=item_id,
                name=name_item,
                description=description_item,
                image=urlimage,
                value=value_item
                )
                
        except:
            print("error")

update_items()
