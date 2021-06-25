import datetime
import threading
import time

import pandas

from trading_freedom_delete import Strategy


def positiontracker(kite, interval):
    from_date = datetime.datetime(2021, 1, 31, 9, 15)
    to_date = datetime.datetime(2021, 2, 18, 15, 15)
    scrip = {}

    for net in kite.positions()["net"]:
        print("Running for", net["tradingsymbol"])
        scrip["instrument_token"] = net["instrument_token"]
        df = downloaddata(kite, from_date, to_date, scrip)
        action = net["quantity"] / abs(net["quantity"])

        Strategy.EX_STRATEGY(df, action, 233.55)

    position_tracker_thread = threading.Timer(interval, positiontracker, [kite])
    position_tracker_thread.start()


def downloaddata(kite, from_date, to_date, scrip):
    token = scrip["instrument_token"]
    time.sleep(1 / 3)  # Rate limit of 3 requests per second

    records = kite.historical_data(instrument_token=token, from_date=from_date, to_date=to_date, interval="15minute")
    df = pandas.DataFrame(data=records)
    df.index = df["date"]
    df.index.name = "timestamp"
    return df
