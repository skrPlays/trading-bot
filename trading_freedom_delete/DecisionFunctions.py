import datetime
import math
import threading
import winsound
from os import name, system

import kiteconnect
import pyttsx3
from termcolor import colored


# Decision on Buy/Sell/Hold
def position_decision(maxProfitPrice, ltp, entryPrice, scripName, orderType, kite):
    exitflag = False
    # engine = pyttsx3.init()
    for i in range(len(maxProfitPrice)):
        if not (scripName[i] == "SBIN" or scripName[i] == "IDEA" or scripName[i] == "TATAPOWER"):
            # system('cls' if name == 'nt' else 'clear')
            max_change_per = (maxProfitPrice[i] - entryPrice[i]) * 100 / entryPrice[i]
            current_change_per = (ltp[i] - entryPrice[i]) * 100 / entryPrice[i]

            print(
                "\033[1m" + scripName[i] + " " + str(datetime.datetime.now()),
                "\033[0mPermissible Pullback: "
                + str(round(permissiblePullback(max_change_per * orderType[i]), 2))
                + "%",
                colored(
                    "Highest Swing: " + str(round(max_change_per, 2)) + "%", "blue" if orderType[i] > 0 else "red"
                ),
                colored(
                    "Current: " + str(round(current_change_per, 2)) + "%", "blue" if current_change_per > 0 else "red"
                ),
                colored(
                    "Distance from Highest: "
                    + str(round((max_change_per - current_change_per) * orderType[i], 2))
                    + "%",
                    "yellow",
                ),
                end=" ",
            )

            exitflag = exitFlag(
                (max_change_per - current_change_per) * orderType[i],
                permissiblePullback(max_change_per * orderType[i]),
            )
            if exitflag:
                # placeorder(kite)
                print(colored("\033[1mExit", "red"))
                # engine.say("Exit "+scripName[i])
                # engine.runAndWait()
                for i in range(0, 5):
                    winsound.Beep(2000, 200)
            else:
                print(colored("\033[1mContinue", "green"))
                # engine.say(scripName[i]+str(round((max_change_per-current_change_per)*orderType[i],2))+"% down")
                # engine.runAndWait()

    return exitflag


# Calculates maximum profit pullback allowed as per the maximum profit level achieved. This will be the STOP LOSS
def permissiblePullback(maxChangePer):
    if maxChangePer < 0.25:
        slPercentage = 1.25
    else:
        slPercentage = 0.4992772 + (1.082036 * math.exp(-1.462251 * maxChangePer))
    return slPercentage


# Determines whether SL has been trigerred or not
def exitFlag(percentageDifferece, permissiblePullback):
    if percentageDifferece > permissiblePullback:
        return True
    else:
        return False


# Placing an order
def placeorder(kite):
    try:
        print(
            kite.place_order(
                transaction_type="BUY",
                quantity=1,
                exchange="NSE",
                tradingsymbol="COALINDIA",
                variety="regular",
                product="MIS",
                order_type="MARKET",
            )
        )
    except kiteconnect.exceptions.KiteException as e:
        print("\nException Encountered:\n", e)
