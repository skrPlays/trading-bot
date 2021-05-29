import json
import time
import pandas
import datetime
import Strategy


def backtest_coordinator_v2 (kite):

    from_date = datetime.datetime(2021, 1, 31, 9, 15)
    initialfund = 100

    for day in {15,16,17,18,19}:
        to_date = datetime.datetime(2021, 2, day, 15, 15)
        print("Executing for:",to_date)
        position_flag = False
        position = {}
        offset = 0

        downloaddata(kite, from_date, to_date)

        for i in range(5,20): # Todo: no position in first few and last few periods
            print("Running Loop",i)
            offset = i-26

            if (position_flag):
                print("Already in position, checking exit condition")
                position_flag, profitpercent = EXIT(offset, position_flag, position)
                initialfund = initialfund*(1 + profitpercent)
            else:
                print("Ready to take new position")
                position["tradingsymbol"], position["action"], position["price"], position_flag = ENTRY(offset, position_flag)

        if position_flag:
            initialfund = initialfund*(1 + settlement(offset, position["tradingsymbol"], position["action"], position["price"]))
        print(initialfund)

    print("Final Profit @5x leverage:",round((initialfund-100)*5,2),"%")
    return


def downloaddata(kite, from_date, to_date):
    with open("C:\wamp\www\TradeFreedom\stocklist.txt", "r") as read_file:
        nifty_list = json.load(read_file)

        for scrip in nifty_list:
            token = scrip['instrument_token']
            time.sleep(1/3) # Rate limit of 3 requests per second

            records = kite.historical_data(instrument_token=token,from_date=from_date,to_date=to_date,interval="15minute")
            # print(records)

            # Plotting CandleStick chart
            df = pandas.DataFrame(data=records)
            df.index = df["date"]
            df.index.name = 'timestamp'
            print("Writing file:",str(scrip["tradingsymbol"]+".csv"))
            df.to_csv("C:\wamp\www\TradeFreedom\BackTesting\HistoricalData\\"+scrip["tradingsymbol"]+".csv")
    return


def ENTRY(offset, position_flag):
    i_sorter = 0
    i_action = "NONE"
    i_scrip = ""
    i_price = 0
    with open("C:\wamp\www\TradeFreedom\stocklist.txt", "r") as read_file:
        nifty_list = json.load(read_file)

    for scrip in nifty_list:
        df_original = pandas.read_csv("C:\wamp\www\TradeFreedom\BackTesting\HistoricalData\\"+scrip["tradingsymbol"]+".csv")
        df_original.index = df_original["date"]
        df_original.index.name = 'timestamp'
        df = df_original.iloc[:len(df_original)+offset+1]

        sorter, action = Strategy.EN_STRATEGY(df)
        if (action == "BUY" or action == "SELL") and sorter > i_sorter:
            print(scrip, action)
            i_action = action
            i_sorter = sorter
            i_scrip = scrip["tradingsymbol"]
            i_price = df["close"][len(df)-1]
            position_flag = True

    print(i_scrip,i_action,i_price,i_sorter)
    return i_scrip, i_action, i_price, position_flag


def EXIT(offset, positionflag, position):

    df_original = pandas.read_csv("C:\wamp\www\TradeFreedom\BackTesting\HistoricalData\\"+position["tradingsymbol"]+".csv")
    df_original.index = df_original["date"]
    df_original.index.name = 'timestamp'
    df = df_original.iloc[:len(df_original)+offset+1]
    profitpercent = 0

    exitflag = Strategy.EX_STRATEGY(df, position["action"], position["price"])

    if exitflag:
        positionflag = False
        profitpercent = settlement(offset, position["tradingsymbol"], position["action"], position["price"])

    return positionflag, profitpercent

def settlement(offset, tradingsymbol, action, entryprice):

    df_original = pandas.read_csv("C:\wamp\www\TradeFreedom\BackTesting\HistoricalData\\"+tradingsymbol+".csv")
    df_original.index = df_original["date"]
    df_original.index.name = 'timestamp'
    df = df_original.iloc[:len(df_original)+offset+1]

    exitprice = df["close"][len(df)-1]
    profit = 0

    if action == "BUY":
        profit = exitprice - entryprice
    elif action == "SELL":
        profit = entryprice - exitprice

    print(tradingsymbol,exitprice,profit/entryprice)
    return profit/entryprice