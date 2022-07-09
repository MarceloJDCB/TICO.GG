from .models import matchObject
from datetime import timedelta
from pytz import timezone
from .dictToJson import dictToJson
from datetime import datetime

def get_match(match_id):
    match = matchObject.objects.get(matchId=match_id)
    # CONVERTING TIMESTAMP TO NORMAL DATE
    # GAME DURATION
    duration = timedelta(seconds=int(match.gameDuration))
    sduration = str(duration)
    gameDuration = sduration[2:len(sduration)]

    timeStamp = float(match.gameEnding)
    gameEnding = datetime.fromtimestamp(timeStamp/1000, tz = timezone("Brazil/East"))
    #DAYS AGO
    EndingDate = datetime(gameEnding.year, gameEnding.month, gameEnding.day, gameEnding.hour, 0, 0)
    #HOURS AGO
    time = (datetime.now() - EndingDate)
    
    days = time.days
    if days > 0:
        x = time.seconds / 86400
        if x > 0.5:
            timeAgo = str(days + 1) + " days ago"
        elif x < 0.5:
            timeAgo = str(days) + " days ago"
    else:
        minutes = time.seconds / 60
        print(minutes)
        if minutes < 60:
            timeAgo = str(minutes) + "minutes ago"
        elif minutes > 60:
            timeAgo = str(round(minutes / 60)) + " hours ago"


    # LOAD THE DATA FROM THE PARTICIPANTS
    PARTICIPANTS_TEXT =  match.participants
    data_participants = dictToJson(PARTICIPANTS_TEXT)
    ##################################################################

    # LOAD THE DATA FROM THE TEAMS
    TEAMS_TEXT =  match.teams   
    data_teams = dictToJson(TEAMS_TEXT)
    ##################################################################

    MATCH_DATA = {
        "gameEnding":match.gameEnding,
        "matchId":match.matchId,
        "category":match.category,
        "gameDuration":gameDuration,
        "timeAgo":timeAgo,
        "participants":data_participants,
        "teams":data_teams
    }
    return (MATCH_DATA)