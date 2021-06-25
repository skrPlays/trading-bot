import threading
import warnings

from kiteconnect import KiteConnect

import v3_Authentication
import v3_Scanner
import v3_Tracker

warnings.filterwarnings("ignore")

# Authenticate
# kite, access_token = v3_Authentication.authenticate()

# Scanner thread activation
scanner_interval = 60 * (1 / 3)
kite = ""
position_tracker_thread = threading.Timer(scanner_interval, v3_Scanner.scan, [kite, scanner_interval])
position_tracker_thread.start()

# Tracking thread activation
tracking_interval = 60 * (1 / 4)
v3_Tracker.track_active_trades(active_trade_list)

# Exit at 00:3:19
# Invoke Timer module to check time and exit all positions at market price
