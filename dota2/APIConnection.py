import urllib2
import json
from dota2Error import Dota2APIError
import time
import random

api_key = 'F14F6FD0544C5151E2E0C7094672A746'
test_api = False

class APIConnection:
    def __init__(self):
        
        # Raise exception if no API key was provided
        if api_key is None:
            raise Dota2APIError('No API key provided')

        # Determine what api version to use
        if test_api is True:
            apiID = '205790'
        else:
            apiID = '570'
            
        self.api_key = api_key
        
        self.match_history_url = 'http://api.steampowered.com/IDOTA2Match_'+apiID+'/GetMatchHistory/V001/?key='+self.api_key
        self.match_detail_url= 'http://api.steampowered.com/IDOTA2Match_'+apiID+'/GetMatchDetails/V001/?key='+self.api_key

        self.match_by_seq_num_url= 'http://api.steampowered.com/IDOTA2Match_'+apiID+'/GetMatchHistoryBySequenceNum/V001/?key='+self.api_key


    def _getData(self, url):
        try:
            time.sleep(random.random())
            response = urllib2.urlopen(url)
            data =  json.load(response)
            return data
        except urllib2.HTTPError as e: 
            if e.code == 401:
                raise Dota2APIError('Invalid API key')
            if e.code == 500:
                time.sleep(2)
                return self._getData(url)
            time.sleep(0.5)
            return self._getData(url)
        except IOError,e:
            print e.args
            time.sleep(0.5)
            return self._getData(url)
        except Exception,e:
            print e.args
            time.sleep(0.5)
            return self._getData(url)

    def searchMatch(self, player_name=None, hero_id=None, game_mode=None, skill=None, date_min=None, 
            date_max=None, min_players=None, account_id=None, leauge_id=None, start_at_match_id=None,
            matches_requested=None, tournament_games_only=None):
            
        # Get arguments
        args = locals()

        # Set request url
        req_url = self.match_history_url

        # Delete reference to self
        del(args['self'])

        # Build url string
        for arg in args.items():
            if arg[1] is not None:
                req_url += '&'+arg[0]+'='+str(arg[1])

        # Get match data
        #jsondata = self._getData(self.match_history_url)
        jsondata = json.load(open('matches.json'))

        # Check result
        if jsondata['result']['status'] != 1:
            raise Dota2APIError(jsondata['result']['statusDetail'])

        # Create dict for result info
        result = {'num_results' : jsondata['result']['num_results'], 'total_results' : jsondata['result']['total_results'], 'results_remaining' : jsondata['result']['results_remaining']};
    

        # Create matches from match data
        matches = list()

        for m in jsondata['result']['matches']:
            matches.append(Match(m))

        # Return result and matches
        return result, matches

    def _getMatchDetails(self, matchID):
        req_url = self.match_detail_url+'&match_id='+str(matchID)

        # Get match data
        jsondata = self._getData(req_url)
        #jsondata = json.load(open('detail.json'))
        return jsondata['result']

    def _getMatchBySeqNum(self, startNum = None):
        req_url = self.match_by_seq_num_url
        if startNum != None:
            req_url += '&start_at_match_seq_num=' + str(startNum);

        jsondata = self._getData(req_url)
        # Check result
        if jsondata['result']['status'] != 1:
            raise Dota2APIError(jsondata['result']['statusDetail'])

        return jsondata['result']['matches'];
