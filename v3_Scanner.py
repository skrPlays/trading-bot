import pandas
import v3_TradeAlgorithmModule
import v3_ConstantLib
import logging

logging.basicConfig(filename=v3_ConstantLib.LOGFILE, level=logging.INFO, format='%(asctime)s - %(message)s')

def scan(kite):
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
    for scrip in nse_list: # TODO: Change to nifty list later
        samplehistorical = open(v3_ConstantLib.SAMPLE_HISTORICAL,'r').read()
        algo_output = v3_TradeAlgorithmModule.tradeAlgorithm(samplehistorical,"newdecision")
        if algo_output['decision'] is 'buy' or algo_output['decision'] is 'sell':
            actionable_queue.append(algo_output)

    print(actionable_queue)
    # TODO: Call sorting function with actionable queue


# Development Section
scan("")