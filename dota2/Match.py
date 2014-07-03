from dota2Error import Dota2APIError 
import time
import datetime
# import dota2
from MysqlHelper import *
from APIConnection import *

class Match():
    _detail_list = (
        'winner', 
        'duration', 
        'tower_status_radiant', 
        'tower_status_dire', 
        'cluster', 
        'first_blood_time', 
        'human_players', 
        'league_id', 
        'positive_votes', 
        'negative_votes', 
        'game_mode', 
        )
    def __init__(self, matchdata):
        # Basic match info
        self.match_id = None
        self.match_seq_num = None
        self.start_time = None
        self.lobby_type = None
        
        if matchdata is not None:
            self.match_id = matchdata['match_id']
            self.match_seq_num = matchdata['match_seq_num']
            self.start_time = time.gmtime(matchdata['start_time'])
            self.lobby_type = self._lobbyType(matchdata['lobby_type'])
            self.players = matchdata['players']

    def __getattr__(self, name):
        if name in self._detail_list:
            self._fetchDetailedData()
            return getattr(self, name)
        else:
            raise AttributeError('Match instance has no attribute ' + name)

    def _fetchDetailedData(self):
        details = APIConnection()._getMatchDetails(self.match_id);

        # Set winner
        if details['radiant_win'] == True:
            self.winner = 'Radiant'
        else:
            self.winner = 'Dire'

        # Make python time of duration
        self.duration = datetime.timedelta(seconds=details['duration'])

        # Set start time
        self.start_time = time.gmtime(details['start_time'])

        # Set tower status
        self.tower_status_radiant = details['tower_status_radiant'] 
        self.tower_status_dire = details['tower_status_dire']

        # Set server cluster
        self.cluster = details['cluster']

        # Set time of first blood
        self.first_blood_time = datetime.timedelta(seconds=details['first_blood_time'])

        # Set number of human players
        self.human_players = details['human_players']
        
        # Set league id
        self.leauge_id = details['leagueid']

        # Set number of positive and negative_votes votes for match
        self.positive_votes = details['positive_votes']
        self.negative_votes = details['negative_votes']

        # Set game mode
        self.game_mode = self._gamemode(details['game_mode'])

    def _gamemode(self, mode):
        if mode == 0:
            return 'None'
        elif mode == 1:
            return 'All Pick'
        elif mode == 2:
            return 'Captain\'s Mode'
        elif mode == 3:
            return 'Random Draft'
        elif mode == 4:
            return 'Single Draft'
        elif mode == 5:
            return 'All Random'
        elif mode == 6:
            return 'Intro'
        elif mode == 7:
            return 'Diretide'
        elif mode == 8:
            return 'Reverse Captain\'s Mode'
        elif mode == 9:
            return 'The Greeviling'
        elif mode == 10:
            return 'Tutorial'
        elif mode == 11:
            return 'Mid Only'
        elif mode == 12:
            return 'Least Played'
        elif mode == 13:
            return 'New Player Pool'
        elif mode == 14:
            return 'Compendium Matchmaking'
        else:
            return 'Unknown game mode'

    def _lobbyType(self, typenum):
        if typenum < 0 and typenum > 6:
            return 'Invalid'
        elif typenum == 0:
            return 'Public matchmaking'
        elif typenum == 1:
            return 'Practise'
        elif typenum == 2:
            return 'Tournament'
        elif typenum == 3:
            return 'Tutorial'
        elif typenum == 4:
            return 'Co-op with bots'
        elif typenum == 5:
            return 'Team match'
        elif typenum == 5:
            return 'Solo Queue'

start_seq_num = 0
handle = MatchHandle()
api = APIConnection()
while True:
    matchs = api._getMatchBySeqNum(start_seq_num)

    for x in matchs:
        match = DotaMatchModel();

        match.match_id            = x['match_id']

        match.match_seq_num       = x['match_seq_num']
        try:
            match.player0                 = str(x['players'][0])
            match.player1                 = str(x['players'][1])
            match.player2                 = str(x['players'][2])
            match.player3                 = str(x['players'][3])
            match.player4                 = str(x['players'][4])
            match.player5                 = str(x['players'][5])
            match.player6                 = str(x['players'][6])
            match.player7                 = str(x['players'][7])
            match.player8                 = str(x['players'][8])
            match.player9                 = str(x['players'][9])
        except Exception, e:
            pass
        else:
            pass
        finally:
            pass
        
        match.radiant_win             = 0 if x['radiant_win'] == False else 1

        match.duration                = x['duration']
        match.start_time              = datetime.datetime.fromtimestamp(
                                            int(x['start_time'])
                                        ).strftime('%Y-%m-%d %H:%M:%S')
        match.first_blood_time        = x['first_blood_time']
        match.tower_status_radiant    = x['tower_status_radiant']
        match.tower_status_dire       = x['tower_status_dire']
        match.barracks_status_radiant = x['barracks_status_radiant']
        match.barracks_status_dire    = x['barracks_status_dire']
        match.cluster                 = x['cluster']
        match.lobby_type              = x['lobby_type']
        match.human_players           = x['human_players']
        match.leagueid                = x['leagueid']
        match.positive_votes          = x['positive_votes']
        match.negative_votes          = x['negative_votes']
        match.game_mode               = x['game_mode']

        handle.saveMatchToDB(match)

        start_seq_num = x['match_seq_num']

    start_seq_num = start_seq_num + 1

        