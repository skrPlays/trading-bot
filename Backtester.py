import json
import time
import HistoricalDataParser
import io
import pandas
import requests
import Scanner
import NewPositionQueue
import DecisionFunctions
import datetime


def bt_scan(kite, from_date, to_date):
    scanresults_file = open("C:\wamp\www\TradeFreedom\scanresults.json", "w")
    with open("C:\wamp\www\TradeFreedom\stocklist.txt", "r") as read_file:
        nifty_list = json.load(read_file)

        for scrip in nifty_list:
            token = scrip['instrument_token']
            time.sleep(1/3) # Rate limit of 3 requests per second

            records = kite.historical_data(instrument_token=token,from_date=from_date,to_date=to_date,interval="15minute")
            with open("C:\wamp\www\TradeFreedom\BackTesting\HistoricalData\\"+scrip["tradingsymbol"]+".txt", "w") as write_file:
                write_file.write(str(records))

            print(records)

            # Plotting CandleStick chart
            df = pandas.DataFrame(data=records)
            df.index = df["date"]
            df.index.name = 'timestamp'

            scrip = Scanner.scanning_str1(scrip, df, 0)

    json.dump(nifty_list,scanresults_file)
    scanresults_file.close()

    return 0

def bt_newposition():
    scannerlist = json.load(open("C:\wamp\www\TradeFreedom\scanresults.json", "r"))
    position_ready = []
    for scrip in scannerlist:
        if not scrip["action"] == "NONE":
            position_ready.append(scrip)

    position_ready = sorted(
        position_ready,
        key = lambda x: x['sort'],
        reverse=True
    )

    return position_ready

def backtest_coordinator(kite):

    from_date = datetime.datetime(2020, 11, 9, 9, 15)
    to_date = datetime.datetime(2020, 11, 20, 15, 15)
    test_to = datetime.datetime(2020, 11, 23, 10, 15)
    intial_fund = 100
    poscount = 0
    negcount = 0
    positions_taken = {}
    backtestfile = open("C:\wamp\www\TradeFreedom\\backtest.txt", "a")
    backtestfile.write("\n")
    # backtestfile.truncate(0)


    while (test_to < datetime.datetime(2020, 11, 23, 10, 30)):
        bt_scan(kite, from_date, test_to)
        sorted_scrips = bt_newposition()
        print(sorted_scrips[0])
        test_to = test_to + datetime.timedelta(minutes=15)


    # TODO: STEP 2
    # position_ready = bt_newposition()
    #
    # initialfund = 100
    # poscount = 0
    # negcount = 0
    # for scrip in position_ready:
    #     records = kite.historical_data(instrument_token=scrip["instrument_token"],from_date=from_date,to_date=to_date,interval="15minute")
    #
    #     idf = pandas.DataFrame(data=records)
    #     idf.index = idf["date"]
    #     idf.index.name = 'timestamp'
    #     flag = NewPositionQueue.entry_str1(scrip, idf, 250, scrip["action"])
    #
    #     test_records = kite.historical_data(instrument_token=scrip["instrument_token"],from_date=test_date,to_date=test_date,interval="15minute")
    #     df = pandas.DataFrame(data=test_records)
    #     df.index = df["date"]
    #     df.index.name = 'timestamp'
    #     max_profit_price = df["open"][0]
    #
    #     i = 0
    #     for close in df["close"]:
    #         ordertype = 1 if scrip["action"] == "BUY" else -1
    #         if ordertype == 1 and flag:
    #             if (close > max_profit_price):
    #                 max_profit_price = close
    #         elif ordertype == 0 and flag:
    #             if (close < max_profit_price):
    #                 max_profit_price = close
    #         if DecisionFunctions.position_decision([max_profit_price],[close],[df["open"][0]],[scrip["tradingsymbol"]],[ordertype],kite):
    #             break
    #         idf.loc[len(idf.index)] = df[i]
    #         i = i+1
    #     print(idf)
    #     if flag:
    #         backtestfile.write("Entry:"+str(df["open"][0])+"Exit:"+str(close)+"Chance %age:"+str(round((close-df["open"][0])*100*ordertype/df["open"][0],2))+"%\n")
    #         print("Entry:",df["open"][0],"Exit:",close,"Chance %age:",str(round((close-df["open"][0])*100*ordertype/df["open"][0],2))+"%")
    #         initialfund = initialfund + round((close-df["open"][0])*100*ordertype/df["open"][0],2)
    #         if (close-df["open"][0])*ordertype > 0:
    #             poscount = poscount + 1
    #         else:
    #             negcount = negcount + 1
    #
    # print(initialfund,poscount,",",negcount,"out of",len(position_ready))
    backtestfile.close()
