from ticorequests import models
from datetime import timedelta, datetime
from .dictToJson import dictToJson
from pytz import timezone

class MatchUtils:
    def __init__(self, match_id):
        self.match = models.MatchObject.objects.get(match_id=match_id)
    
    def get_match_json(self):
        time_ago,game_duration = self.calculate_match_ending_days_and_game_duration()

        match_data = {
            "matchId":self.match.match_id,
            "category":self.match.category,
            "gameDuration":game_duration,
            "timeAgo":time_ago,
            "participants":self.format_participants_textfield(),
            "teams":self.format_teams_textfield()
        }
        return match_data

    def get_specific_player_match(self,player_puuid):

        participant = None
        for player in self.format_participants_textfield():
            if player['puuid'] == player_puuid:
                participant = player
        
        if participant is None:
            raise Exception("Player not found in the requested match")

        return {"participant":participant}

    def format_participants_textfield(self):
        return dictToJson(self.match.participants)
    
    def format_teams_textfield(self):
        return dictToJson(self.match.teams)

    def calculate_match_ending_days_and_game_duration(self):
        # CONVERTING TIMESTAMP TO NORMAL DATE
        # GAME DURATION
        duration = str(timedelta(seconds=int(self.match.game_duration)))
        game_duration = duration[2:len(duration)]

        time_stamp = (float(self.match.game_ending) / 1000)
        game_ending_date = datetime.fromtimestamp(time_stamp, tz=timezone("Brazil/East"))
        ending_date = datetime(game_ending_date.year, game_ending_date.month, game_ending_date.day, game_ending_date.hour, 0, 0)
        result_time = (datetime.now() - ending_date)

        days = result_time.days
        if days > 0:
            x = result_time.seconds / 86400
            if x > 0.5:
                time_ago = str(days + 1) + " days ago"
            elif x < 0.5:
                time_ago = str(days) + " days ago"
        else:
            minutes = result_time.seconds / 60
            if minutes < 60:
                time_ago = str(minutes) + "minutes ago"
            elif minutes > 60:
                time_ago = str(round(minutes / 60)) + " hours ago"
        
        return time_ago,game_duration

class MatchTimelineUtils:
    def __init__(self, match_id):
        self.match_timeline = models.MatchTimeLineObject.objects.get(match_id=match_id)
    
    def format_events_textfield(self):
        return dictToJson(self.match_timeline.all_events)

    def get_player_timeline(self,player_name):
        events_player = []
        for data in self.format_events_textfield():
            if data["participantId"] == player_name:
                events_player.append(data)
        return events_player
        