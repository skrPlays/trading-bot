import logging
import threading

import pandas

import v3_ConstantLib
import v3_Entry
import v3_Sort
import v3_TradeAlgorithmModule

logging.basicConfig(filename=v3_ConstantLib.LOGFILE, level=logging.INFO, format="%(asctime)s - %(message)s")


def scan(kite, interval):
    # Reading list of stocks from NSE India
    nse_list = pandas.read_csv("https://www1.nseindia.com/content/indices/ind_nifty500list.csv")
    print(nse_list)
    nifty_list = []
    actionable_queue = []

    # Reading 'instrument token' from the Kite Library
    # for scrip in kite.instruments("NSE"):
    #     if scrip['instrument_type'] == "EQ" and scrip["segment"] == "NSE" and (scrip['tradingsymbol'] in nifty500['Symbol'].values):
    #         nifty_list.append({"instrument_token":scrip['instrument_token'],"tradingsymbol":scrip['tradingsymbol']})

    # Reading through the list and sending to algo for initial testing
    for scrip in nse_list:  # TODO: Change to nifty list later
        samplehistorical = open(v3_ConstantLib.SAMPLE_HISTORICAL, "r").read()
        algo_output = v3_TradeAlgorithmModule.tradeAlgorithm(samplehistorical, "newdecision")
        if algo_output["decision"] is "buy" or algo_output["decision"] is "sell":
            actionable_queue.append(algo_output)

    print(actionable_queue)
    print("Sort Function:", v3_Sort.sort(actionable_queue))

    # Call sorting function with actionable queue
    sorted_algo_output = v3_Sort.sort(actionable_queue)

    # Invoking Entry module
    v3_Entry.take_entry(sorted_algo_output, samplehistorical)

    # Re-calling scanner after interval
    position_tracker_thread = threading.Timer(interval, scan, [kite, interval])
    position_tracker_thread.start()
    return 0
