from .models import matchObject
from .dictToJson import dictToJson

def player_match(match_id,playerpuuid):
    
    match = matchObject.objects.get(matchId=match_id)
    # LOAD THE DATA FROM THE PARTICIPANT
    PARTICIPANTS_TEXT =  match.participants
    data_participants = dictToJson(PARTICIPANTS_TEXT)
    participant = ""
    for player in data_participants:
        if player['puuid'] == playerpuuid:
            participant = player
        else:
            continue                   
    ##################################################################

    MATCH_DATA = {
        "participant":participant,
    }
    return (MATCH_DATA)