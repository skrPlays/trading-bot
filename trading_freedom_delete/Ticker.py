#!python
import json

from kiteconnect import KiteConnect, KiteTicker

# import pyttsx3


def startticker(api_key, access_token):
    # Declare
    instrument_token = []
    ltp_json = {}

    # Initialise
    kws = KiteTicker(api_key, access_token)
    kite = KiteConnect(api_key)
    kite.set_access_token(access_token)
    for net in kite.positions()["net"]:
        instrument_token.append(net["instrument_token"])

    def on_ticks(ws, ticks):
        # print("Ticks Received:",ticks)
        for intrumentltp in ticks:
            ltp_json[intrumentltp["instrument_token"]] = intrumentltp["last_price"]

        # Making sure that all current positions are subscribed
        for net in kite.positions()["net"]:
            if not (net["instrument_token"] in ltp_json):
                print("New Subscription:", net["instrument_token"])
                ws.subscribe([net["instrument_token"]])

        with open("C:\wamp\www\TradeFreedom\ltptracker.json", "w") as write_file:
            json.dump(ltp_json, write_file)

    def on_connect(ws, response):
        ws.subscribe(instrument_token)
        ws.set_mode(ws.MODE_LTP, instrument_token)
        universal_kws = ws

    def on_close(ws, code, reason):
        print(reason)
        # ws.stop()

    def on_error(ws, code, reason):
        print(reason)

    def on_reconnect(ws, attempts_count):
        print(attempts_count)

    # Assign the callbacks.
    kws.on_ticks = on_ticks
    kws.on_connect = on_connect
    kws.on_close = on_close
    kws.on_error = on_error
    kws.on_reconnect = on_reconnect

    # Infinite loop on the main thread. Nothing after this will run.
    # You have to use the pre-defined callbacks to manage subscriptions.
    kws.connect()
