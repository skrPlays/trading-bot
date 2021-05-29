from kiteconnect import KiteConnect
import pandas
import json
import threading
import time
import requests
import Ticker
import PositionTracker
import datetime
import HistoricalDataParser
import Scanner
import NewPositionQueue
import Backtester
import Backtester_v2
import NewPositionTracker

import warnings
warnings.filterwarnings("ignore")

# Variable Declarations/Initializations
api_key = "1pb2l0oc8cnx45l7"
api_secret = "tzvlq8pvg58z97qzz8k5f5iqwo59nfo7"
kite = KiteConnect(api_key)
position_tracker_interval = 10
scanner_interval = 60*15
log_file_name = "C:\wamp\www\TradeFreedom\logs\\"+str(datetime.date.today())+"_logfile.log"
log_file = open(log_file_name,"a")


# Obtaining Access Token
login = requests.get(kite.login_url())
cookies = ';'.join(['%s=%s'%(k,v) for k, v in login.history[1].cookies.items()])
headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0',
        "X-Kite-Userid": 'YJ5684', 'X-Kite-Version': '2.4.0',
        'Cookie': cookies, 'Referer': login.url
    }
data = requests.post("https://kite.zerodha.com/api/login",{'user_id':"YJ5684",'password':"<>"},headers=headers)
data = requests.post("https://kite.zerodha.com/api/twofa",{'user_id':"YJ5684",'request_id':data.json()['data']['request_id'],'twofa_value':},headers=headers)

public_token = data.cookies.get_dict()['public_token']
user_id='user_id='+"YJ5684"
headers.update({'Cookie': cookies+';'+'public_token='+public_token+';'+user_id})
data = requests.get(login.url+'&skip_session=true', headers=headers)
request_token = data.url.split("request_token")[1].split("=")[1]
if  "&" in request_token:
    request_token = request_token.split("&")[0]

data = kite.generate_session(request_token, api_secret)
access_token = data['access_token']
kite.set_access_token(access_token)
print("Access Token: ",access_token)

# NIFTY 500: Reads all stocks in NIFTY 500 from their website, and fetches corresponding instrument tokens from Kite
#
#
# nifty500 = pandas.read_csv("https://www1.nseindia.com/content/indices/ind_nifty100list.csv")
nifty500 = pandas.read_csv("https://www1.nseindia.com/content/indices/ind_nifty500list.csv")
nifty_list = []
for scrip in kite.instruments("NSE"):
    if scrip['instrument_type'] == "EQ" and scrip["segment"] == "NSE" and (scrip['tradingsymbol'] in nifty500['Symbol'].values):
        nifty_list.append({"instrument_token":scrip['instrument_token'],"tradingsymbol":scrip['tradingsymbol']})

with open("C:\wamp\www\TradeFreedom\stocklist.txt", "w") as write_file:
    json.dump(nifty_list, write_file)
#
# End Block
# _______________________________________________________________________________________________________________________________


# Scanner: Runs every N Minutes
#
#
# scanner_thread = threading.Timer(0, Scanner.scan_and_sort,[kite, scanner_interval])
# scanner_thread.start()
#
# End Block
# _______________________________________________________________________________________________________________________________


# NewPositionQueue.position_queue(kite)


# Position Tracker: Runs every N seconds
#
#
# position_tracker_thread = threading.Timer(position_tracker_interval, PositionTracker.trackpositions,[api_key,access_token, position_tracker_interval, kite])
# position_tracker_thread.start()
# position_tracker_thread = threading.Timer(position_tracker_interval, NewPositionTracker.positiontracker,[kite, position_tracker_interval])
# position_tracker_thread.start()
#
# End Block
# _______________________________________________________________________________________________________________________________


# Ticker: Connects to Kiteticker
#
#
# Ticker.startticker(api_key,access_token) # TODO: SUBSCRIBE TO ALL
#
# End Block
# _______________________________________________________________________________________________________________________________


Backtester_v2.backtest_coordinator_v2(kite)