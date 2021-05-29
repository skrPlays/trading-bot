import HistoricalDataParser
import pandas
import mplfinance
import threading
import json
import ta
import time

def scan_and_sort(kite, scanner_interval):

    scanresults_file = open("C:\wamp\www\TradeFreedom\scanresults.json", "w")

    with open("C:\wamp\www\TradeFreedom\stocklist.txt", "r") as read_file:
        nifty_list = json.load(read_file)

    interval = '15minute'
    period = 500
    offset = 0
    ltp_json = {}

    for scrip in nifty_list:
        token = scrip['instrument_token']
        time.sleep(1/3) # Rate limit of 3 requests per second

        records_trimmed, timestamp, Open, high, low, close, volume = \
            HistoricalDataParser.read_historical_data(kite=kite,token=token,interval=interval,period=period,offset=offset)

        # Plotting CandleStick chart
        df = pandas.DataFrame(index=timestamp,data=records_trimmed)
        df.index.name = 'date'

        scrip = scanning_str1(scrip, df, period)
        ltp_json[scrip["instrument_token"]] = df["close"][len(df)-1]

        # mavdf = pandas.DataFrame(dict(mav_long=mav_long,mav_med=mav_med,mav_short=mav_short,bb_mav=bb_mav,bb_hband=bb_hband,bb_lband=bb_lband),
        #                          index=df.index)
        # ap = mplfinance.make_addplot(mavdf,type='line')
        # mplfinance.plot(df ,type='candle',addplot=ap,volume=True)

    json.dump(nifty_list,scanresults_file)
    scanresults_file.close()
    with open("C:\wamp\www\TradeFreedom\ltptracker.json", "w") as write_file:
            json.dump(ltp_json, write_file)


    scanner_thread = threading.Timer(scanner_interval, scan_and_sort,[kite, scanner_interval])
    scanner_thread.start()

def sorter(nifty_list):
    return nifty_list['sort']

def scanning_str1(scrip, df, period):
    # Exponential Moving Averages
    # mav_long = ta.trend.EMAIndicator(close=df["close"],n=int(period*0.75)).ema_indicator()
    # mav_med = ta.trend.EMAIndicator(close=df["close"],n=int(period*0.5)).ema_indicator()
    # mav_short = ta.trend.EMAIndicator(close=df["close"],n=int(period*0.25)).ema_indicator()
    vol_ema = ta.trend.EMAIndicator(close=df["volume"],n=20).ema_indicator()

    # MACD
    adx = ta.trend.ADXIndicator(high=df["high"], low=df["low"], close=df["close"], n=14).adx()
    pdi = ta.trend.ADXIndicator(high=df["high"], low=df["low"], close=df["close"], n=14).adx_pos()
    ndi = ta.trend.ADXIndicator(high=df["high"], low=df["low"], close=df["close"], n=14).adx_neg()

    #Bollinger Bands
    bb_mav = ta.volatility.BollingerBands(close=df["close"], n=20, ndev=2).bollinger_mavg()
    bb_hband = ta.volatility.BollingerBands(close=df["close"], n=20, ndev=2).bollinger_hband()
    bb_lband = ta.volatility.BollingerBands(close=df["close"], n=20, ndev=2).bollinger_lband()

    pn_diratio = pdi[len(pdi)-1]/ndi[len(ndi)-1]
    np_diratio = ndi[len(ndi)-1]/pdi[len(pdi)-1]

    if (pn_diratio>2.5):
        scrip["action"] = "BUY"
    elif (np_diratio>2.5):
        scrip["action"] = "SELL"
    else:
        scrip["action"] = "NONE"

    scrip["sort"] = int(df["volume"][len(df["volume"])-1])

    return scrip