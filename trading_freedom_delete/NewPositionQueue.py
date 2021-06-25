import json

import pandas
import ta

from trading_freedom_delete import HistoricalDataParser


# first read all tradable instruments from scanner output. queue them here and track ltp. if they reach a position where we can enter,
# put them in the position queue. then check balance and implement order accordingly
def position_queue(kite):
    margin = kite.margins()["equity"]["net"]
    marginbuffer = 10000
    scannerlist = json.load(open("C:\wamp\www\TradeFreedom\scanresults.json", "r"))

    position_ready = []
    for scrip in scannerlist:
        if not scrip["action"] == "NONE":
            position_ready.append(scrip)

    position_ready = sorted(position_ready, key=lambda x: x["sort"], reverse=True)

    for scrip in position_ready:
        period = 500
        records_trimmed, timestamp, Open, high, low, close, volume = HistoricalDataParser.read_historical_data(
            kite=kite, token=scrip["instrument_token"], interval="15minute", period=period, offset=0
        )
        # Plotting CandleStick chart
        df = pandas.DataFrame(index=timestamp, data=records_trimmed)
        df.index.name = "date"
        entry_str1(scrip, df, period, scrip["action"])


def entry_str1(scrip, df, period, action):

    # Exponential Moving Averages
    mav_long = ta.trend.EMAIndicator(close=df["close"], n=int(period * 0.75)).ema_indicator()
    mav_med = ta.trend.EMAIndicator(close=df["close"], n=int(period * 0.5)).ema_indicator()
    mav_short = ta.trend.EMAIndicator(close=df["close"], n=int(period * 0.25)).ema_indicator()
    vol_ema = ta.trend.EMAIndicator(close=df["volume"], n=20).ema_indicator()

    # MACD
    adx = ta.trend.ADXIndicator(high=df["high"], low=df["low"], close=df["close"], n=14).adx()
    pdi = ta.trend.ADXIndicator(high=df["high"], low=df["low"], close=df["close"], n=14).adx_pos()
    ndi = ta.trend.ADXIndicator(high=df["high"], low=df["low"], close=df["close"], n=14).adx_neg()

    # Bollinger Bands
    bb_mav = ta.volatility.BollingerBands(close=df["close"], n=20, ndev=2).bollinger_mavg()
    bb_hband = ta.volatility.BollingerBands(close=df["close"], n=20, ndev=2).bollinger_hband()
    bb_lband = ta.volatility.BollingerBands(close=df["close"], n=20, ndev=2).bollinger_lband()

    # MACD
    macd = ta.trend.MACD(close=df["close"], n_slow=26, n_fast=12, n_sign=9, fillna=False).macd()
    macd_sig = ta.trend.MACD(close=df["close"], n_slow=26, n_fast=12, n_sign=9, fillna=False).macd_signal()

    an_diratio = adx[len(adx) - 1] / ndi[len(ndi) - 1]
    ap_diratio = adx[len(adx) - 1] / pdi[len(pdi) - 1]

    close = df["close"]
    lnx = len(df) - 1

    buymomentum = (adx[lnx] > 35) and (macd[lnx] > 0) and {macd[lnx] > macd_sig[lnx]}
    sellmomentum = (adx[lnx] > 35) and (macd[lnx] < 0) and {macd[lnx] < macd_sig[lnx]}

    buyflag = (action == "BUY") and buymomentum
    sellflag = (action == "SELL") and sellmomentum

    if buyflag:
        print("Buy", scrip["tradingsymbol"])
        return buyflag
    elif sellflag:
        print("Sell", scrip["tradingsymbol"])
        return sellflag

    return False
