from dota2Error import Dota2APIError 
import time
import datetime
# import dota2
from MysqlHelper import *
from APIConnection import *
from multiprocessing import Process, Queue, Lock, freeze_support
import time
import random

start_seq_num = 0
handle = MatchHandle()
api = APIConnection()

process_num = 5
base_num = 1000000
base_start_num = 200000000
base_end_num  = 650000000
max_process_num = (base_end_num - base_start_num) / base_num

def fetch_history_by_seq_num(data_queue, start_seq_num, callback_queue):
    max_seq_num = start_seq_num + base_num
    while True:
        matchs = api._getMatchBySeqNum(start_seq_num)

        for x in matchs:
            while data_queue.full():
                time.sleep(random.random())
            
            data_queue.put(x)
            start_seq_num = x['match_seq_num']

        start_seq_num += 1

        if start_seq_num >= max_seq_num:
            callback_queue.put(1)
            break

def saveToDB(queue):
    while True:
        x = queue.get()
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

    start_seq_num = start_seq_num + 1



if __name__ == '__main__':
    freeze_support()

    process_list = []

    q = Queue()
    callback_queue = Queue()


    for i in xrange(0,process_num):
        process_list.append(Process(target=fetch_history_by_seq_num,args=(q, base_start_num + base_num * i, callback_queue,)))

    current_num = process_num

    process_list.append(Process(target=saveToDB,args=(q,)))

    for x in process_list:
        x.start()

    result =  callback_queue.get()
    while result == 1:
        print current_num
        if current_num >= max_process_num:
            break
        Process(target=fetch_history_by_seq_num,args=(q, base_start_num + base_num * current_num, callback_queue,)).start()
        current_num += 1
        result = callback_queue.get()

    for x in process_list:
        x.join()
