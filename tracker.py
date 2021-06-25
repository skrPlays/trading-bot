"""
@author: some_cool_dude
"""

import exit
import trade_algorithm


def init_ticker(active_trade_list):
    data_stream = {}

    if """Check if ticker is being initialized for the first time""":
        # Invoke some Kite function
        data_stream = {}  # Store data locally ??
    elif """Check if new scrip is added to the active trade list""":
        # Invoke some Kite function to fetch data specific to the missing scrip
        stream = {}
        data_stream = data_stream.update(stream)  # Store data locally ??
    else:
        x = 0  # Do nothing

    # Warning when stream breaks

    return data_stream


def is_indicator_exit(scrip):
    is_exit = False

    # Invoke Algo module probably
    is_exit = trade_algorithm.get_indicator_decision(scrip)

    return is_exit


def track_active_trades(active_trade_list):
    # Initialize ticker sub-module for all scanner stocks (Reads live stream)
    init_ticker(active_trade_list)

    for scrip in active_trade_list:
        # Step 1: Exit if SL hit
        if """Check if current PA is equal or less than the defined SL""":
            exit.exit_trade(scrip)  # Do we really need to use this ??
        # Step 2: Exit when target is hit
        elif """#Check if current PA is equal or greater than the defined target""":
            exit.exit_trade(scrip)  # Can we instead use CO in zerodha ??
        # Step 3: Check if PA is favourable to our trade, define trailing SL
        elif """Check if current PA is equal or greater than our entry price""":
            x = 0  # Invoke the Kite function to modify SL price
        # Step 4: Indicator-based exit
        elif is_indicator_exit(scrip):
            exit.exit_trade(scrip)
