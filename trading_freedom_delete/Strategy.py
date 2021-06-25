import kiteconnect
import numpy
import ta

from trading_freedom_delete import DecisionFunctions


def EN_STRATEGY(df):

    lnx = len(df) - 1
    close = df["close"]

    turnover = df["volume"][lnx] * df["close"][lnx]

    # Exponential Moving Averages
    ema_volume = ta.trend.EMAIndicator(close=df["volume"], n=50).ema_indicator()
    ema_long = ta.trend.EMAIndicator(close=df["close"], n=250).ema_indicator()
    ema_short = ta.trend.EMAIndicator(close=df["close"], n=250).ema_indicator()

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

    adx_buy_diratio = adx[lnx] / ndi[lnx]
    adx_sell_diratio = adx[lnx] / pdi[lnx]

    # Miscellaneous limits
    bollingersplit = (bb_hband[lnx] - bb_lband[lnx]) < numpy.nanmax([i - j for i, j in zip(bb_hband, bb_lband)]) / 2
    miscellaneousflag = bollingersplit

    # Bollinger combo
    buybollinger = (
        (close[lnx - 2] < bb_hband[lnx - 2]) and (close[lnx - 1] > bb_hband[lnx - 1]) and (close[lnx] < bb_hband[lnx])
    )
    sellbollinger = (
        (close[lnx - 2] > bb_lband[lnx - 2]) and (close[lnx - 1] < bb_lband[lnx - 1]) and (close[lnx] > bb_lband[lnx])
    )

    # Other combos
    buyother = (close[lnx] > ema_long[lnx]) and (adx_buy_diratio > 2.5)
    sellother = (close[lnx] < ema_long[lnx]) and (adx_sell_diratio > 2.5)

    # buyflag = buybollinger and buyother and miscellaneousflag
    # sellflag = sellbollinger and sellother and miscellaneousflag

    # Streak simple strategy
    buyflag = (
        (adx_buy_diratio > 2.5)
        and (close[lnx - 2] < bb_hband[lnx - 2])
        and (close[lnx - 1] > bb_hband[lnx - 1])
        and (close[lnx] < bb_hband[lnx])
    )
    sellflag = (
        (adx_sell_diratio > 2.5)
        and (close[lnx - 2] > bb_lband[lnx - 2])
        and (close[lnx - 1] < bb_lband[lnx - 1])
        and (close[lnx] > bb_lband[lnx])
    )

    if buyflag:
        action = "BUY"
    elif sellflag:
        action = "SELL"
    else:
        action = "NONE"

    sorter = turnover

    return sorter, action


def EX_STRATEGY(df, action, entryprice):

    lnx = len(df) - 1
    close = df["close"]
    ordertype = 0 if action == "SELL" else 1
    bollinger_profit = False
    bollinger_exit = False
    macd_exit = False

    # Bollinger Bands
    bb_mav = ta.volatility.BollingerBands(close=df["close"], n=20, ndev=2).bollinger_mavg()
    bb_hband = ta.volatility.BollingerBands(close=df["close"], n=20, ndev=2).bollinger_hband()
    bb_lband = ta.volatility.BollingerBands(close=df["close"], n=20, ndev=2).bollinger_lband()

    # MACD
    macd = ta.trend.MACD(close=df["close"], n_slow=26, n_fast=12, n_sign=9, fillna=False).macd()
    macd_sig = ta.trend.MACD(close=df["close"], n_slow=26, n_fast=12, n_sign=9, fillna=False).macd_signal()

    if action == "BUY":
        bollinger_profit = close[lnx] > bb_hband[lnx]
        bollinger_exit = (close[lnx] < bb_mav[lnx]) and (close[lnx - 1] < bb_mav[lnx - 1])
        macd_exit = macd[lnx] < macd_sig[lnx]
    elif action == "SELL":
        bollinger_profit = close[lnx] < bb_lband[lnx]
        bollinger_exit = (close[lnx] > bb_mav[lnx]) and (close[lnx - 1] > bb_mav[lnx - 1])
        macd_exit = macd[lnx] > macd_sig[lnx]

    losslimitflag = readlosslimitflag(df, close, lnx, entryprice, ordertype)

    profitbooking = bollinger_profit
    unfavourabletrade = losslimitflag and (macd_exit or bollinger_exit)
    exitflag = profitbooking or unfavourabletrade

    if exitflag:
        print("Exit Flagged")

    return exitflag


def readlosslimitflag(df, close, lnx, entryprice, ordertype):

    if ordertype == 1:
        maxprofitprice = max(close[(df[df["close"] == entryprice].index.values[0]) :])
    else:
        maxprofitprice = min(close[(df[df["close"] == entryprice].index.values[0]) :])

    flag = DecisionFunctions.position_decision(
        [maxprofitprice], [close[lnx]], [entryprice], ["WHATEVS"], [ordertype], kiteconnect.KiteConnect
    )

    return flag
