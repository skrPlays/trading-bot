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


def getNewTradeDecision(historical):
    tradeDecision = "buy"
    sortingValue, sortingType = getSortingValueType(historical)
    return tradeDecision, sortingValue, sortingType


def getSortingValueType(historical):
    sortingValue = 0
    sortingType = "asc"
    return sortingValue, sortingType


def getTradeTrackingDecision(historical):
    return "reversal"


def tradeAlgorithm(historical, operation):
    logging.info('Trade Algorithm Module called with operation - '+operation)
    if(operation is "newdecision"):
        return getNewTradeDecision(historical)
    elif (operation is "trackreversal"):
        return getTradeTrackingDecision(historical)


# Development Section
logging.basicConfig(filename=v3_ConstantLib.LOGFILE, level=logging.INFO, format='%(asctime)s - %(message)s')
samplehistorical = open(v3_ConstantLib.SAMPLE_HISTORICAL,'r').read()
print(tradeAlgorithm(samplehistorical,"newdecision"))
print(samplehistorical)