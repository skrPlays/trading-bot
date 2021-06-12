from kiteconnect import KiteConnect
import v3_Authentication
import threading
import v3_Scanner

import warnings
warnings.filterwarnings("ignore")

# Authenticate
# kite, access_token = v3_Authentication.authenticate()

# Scanner thread activation
scanner_interval = 60*(1/12)
kite=""
position_tracker_thread = threading.Timer(scanner_interval, v3_Scanner.scan,[kite, scanner_interval])
position_tracker_thread.start()

# Tracking thread activation
tracking_interval = 60*(1/4)