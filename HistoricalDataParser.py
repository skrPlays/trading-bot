import datetime
import math
import pandas
import mplfinance

def read_historical_data(kite, token, interval, period, offset):

    open = []
    close = []
    high = []
    low = []
    volume = []
    timestamp = []

    from_timestamp = get_from_timestamp(interval, period, offset)
    print("Fetching data from: ",from_timestamp,", to: ",datetime.datetime.now(),sep='')

    records = kite.historical_data(instrument_token=token,from_date=from_timestamp,to_date=datetime.datetime.now(),interval=interval)
    records_trimmed = trim_records(records, period, offset)

    for ohlc in records_trimmed:
        open.append(ohlc['open'])
        close.append(ohlc['close'])
        high.append(ohlc['high'])
        low.append(ohlc['low'])
        volume.append(ohlc['volume'])
        timestamp.append(ohlc['date'])

    # Plotting CandleStick chart
    # df = pandas.DataFrame(index=timestamp,data=records_trimmed)
    # df.index.name = 'Date'
    # print(df)
    # mplfinance.plot(df, type='candle',volume=True)

    return records_trimmed, timestamp, open, high, low, close, volume

def get_from_timestamp(interval, periods, offset):
    if 'minute' in interval:
        days = math.ceil((periods+offset)/6)
        delta = datetime.timedelta(days=days*2)
        return datetime.datetime.now() - delta
    elif 'day' in interval:
        days = periods+offset
        delta = datetime.timedelta(days=days*2)
        return datetime.datetime.now() - delta
    elif 'week' in interval:
        days = (periods+offset)*7
        delta = datetime.timedelta(days=days*2)
        return datetime.datetime.now() - delta
    elif 'month' in interval:
        days = (periods+offset)*31
        delta = datetime.timedelta(days=days*2)
        return datetime.datetime.now() - delta

def trim_records(records, periods, offset):
    length = len(records)
    return records[length-offset-periods:length-offset]