# Description: This function houses all the user defined algorithms that use
# indicators and price action to decide trading decisions for a stock.
# Inputs:
# Historical Stock Data (historical) - DataFrame
# Operation to perform on data (operation) - String {"newdecision","trackreversal",}
# Outputs:
# Trade Decision (tradeDecision) - String {"buy","sell","none"} in "newdecision" mode/{"reversal","none"} in "trackreversal" mode
# Sorting Value (sortingValue) - Double
# Sorting Type (sortingType) - String {"asc","desc"}

import v3_ConstantLib
import logging

logging.basicConfig(filename=v3_ConstantLib.LOGFILE, level=logging.INFO, format='%(asctime)s - %(message)s')

def getNewTradeDecision(historical):
    decision = "buy"
    sortvalue = getSortingValueType(historical)
    return decision, sortvalue


def getSortingValueType(historical):
    sortingValue = 0
    return sortingValue


def getTradeTrackingDecision(historical):
    return "reversal"


def tradeAlgorithm(historical, operation):
    logging.info('Trade Algorithm Module called with operation - '+operation)
    scrip_info = {}

    scrip_info['instrument_token'] = 1011007
    scrip_info['tradingsymbol'] = "THEGREATJ"

    # Calling functions based on operation needed from the algo
    if(operation is "newdecision"):
        scrip_info['decision'], scrip_info['sortvalue'] = getNewTradeDecision(historical)
    elif (operation is "trackreversal"):
        scrip_info['decision'] = getTradeTrackingDecision(historical)
        scrip_info['sortvalue'] = 0

    # Returning required information
    return scrip_info


