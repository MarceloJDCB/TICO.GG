import requests
from .models import runesObject

def save_rune(rune_id,rune_key,rune_icon,rune_name,rune_desc):
    try:
        rune = runesObject.objects.get(runeId=rune_id)
        rune.key = rune_key
        rune.icon = rune_icon
        rune.name = rune_name
        rune.description = rune_desc
        rune.save()
    except:
        try:
            obj, created = runesObject.objects.update_or_create(
                runeId=rune_id,
                key=rune_key,
                icon=rune_icon,
                name=rune_name,
                description=rune_desc
            )
        except:
            print("error")

def update_runes():
    # CREATING PARAMETERS TO GET THE ACTUAL VERSION OF DATA DRAGON AND LANGUAGE
    dragon_version_response = requests.get('https://ddragon.leagueoflegends.com/api/versions.json').json()
    actual_version = dragon_version_response[0]
    selected_language = "pt_BR"

    # GETTING INFO FOR THE RUNES
    info_runes_response = requests.get(f'https://ddragon.leagueoflegends.com/cdn/{actual_version}/data/{selected_language}/runesReforged.json').json()


    for i in range(0,len(info_runes_response)):
        # CATCHING INFORMATION FROM THE PRINCIPAL TREE
        Id = (info_runes_response[i]['id'])
        Key = (info_runes_response[i]['key'])
        Icon = (info_runes_response[i]['icon'])
        Name = (info_runes_response[i]['name'])
        Desc = ""        
        save_rune(Id,Key,Icon,Name,Desc)
        
        slots = info_runes_response[i]['slots']
        for slot in slots:
            runes = slot['runes']
            for rune in runes:
                Id = rune['id']
                Key = rune['key']
                Icon = rune['icon']
                Name = rune['name']
                Desc = rune['longDesc']
                save_rune(Id,Key,Icon,Name,Desc)
        
        
update_runes()

