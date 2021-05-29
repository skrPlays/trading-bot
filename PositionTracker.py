import threading
import json
from kiteconnect import KiteConnect
import DecisionFunctions
import datetime

def trackpositions(api_key,access_token,interval,kite):

    maxprofit_filename = "C:\wamp\www\TradeFreedom\logs\\"+str(datetime.date.today())+"_max_profit_tracker.json"
    ltptracker_filename = "C:\wamp\www\TradeFreedom\ltptracker.json"

    # Reading LTP as reported by the Ticker
    try:
        f = open(ltptracker_filename, "r")
        ltpresponse = json.loads(f.read())
        f.close()
    except:
        trackpositions(api_key,access_token,interval,kite)

    # Reading Max Profit stored info
    try:
        f = open(maxprofit_filename, "r")
        max_profit_json = json.loads(f.read())
        f.close()
    except:
        max_profit_json = {}

    #Reading currently held positions from Kite Account
    instrument_token = []
    scrip_name = []
    order_type = []
    entry_price = []
    last_price = []
    max_profit_price = []

    # responsetest = requests.post("http://127.0.0.1/tradefreedom/EchoPositionResponse.php").json() # For Off-market testing
    for net in kite.positions()["net"]:
        instrument_token.append(net["instrument_token"])
        scrip_name.append(net["tradingsymbol"])
        order_type.append(0 if net["quantity"]==0 else net["quantity"]/abs(net["quantity"]))

        # If no LTP data for the token exists, we add a default value manually
        if not (str(net["instrument_token"]) in ltpresponse):
            ltpresponse[str(net["instrument_token"])] = 0

        if  net["quantity"] != 0:
            if net["quantity"]/abs(net["quantity"]) == 1:
                entry_price.append(net["buy_price"])
                max_profit_price.append(max_profit_json[str(net["instrument_token"])]) if str(net["instrument_token"]) in max_profit_json else max_profit_price.append(net["buy_price"])
                last_price.append(ltpresponse[str(net["instrument_token"])])
            elif net["quantity"]/abs(net["quantity"]) == -1:
                entry_price.append(net["sell_price"])
                max_profit_price.append(max_profit_json[str(net["instrument_token"])]) if str(net["instrument_token"]) in max_profit_json else max_profit_price.append(net["sell_price"])
                last_price.append(ltpresponse[str(net["instrument_token"])])

    # Now the positions have been read and all info is stored in relevant arrays
    # This section reads through all instrument tokens, checks if new price as reported by LTP Tracker is better than currently stored best price
    # Updates the stored max profit price if new price is better

    for i in range(len(instrument_token)):
        if order_type[i] == 1:
            if (last_price[i] > max_profit_price[i]):
                max_profit_price[i] = last_price[i]
                max_profit_json[str(instrument_token[i])] = max_profit_price[i]
        elif order_type[i] == -1:
            if (last_price[i] < max_profit_price[i]):
                max_profit_price[i] = last_price[i]
                max_profit_json[str(instrument_token[i])] = max_profit_price[i]

    # Writing updated max prices to the output file
    with open(maxprofit_filename, "w") as write_file:
            json.dump(max_profit_json, write_file)

    # Sends all information to Decision Function to check whether to stay in position or exit
    DecisionFunctions.position_decision(max_profit_price,last_price,entry_price,scrip_name,order_type,kite)


    position_tracker_thread = threading.Timer(interval, trackpositions, [api_key, access_token, interval, kite])
    position_tracker_thread.start()