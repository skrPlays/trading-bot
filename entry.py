"""
@author: some_cool_dude
"""
import tracker
import trade_algorithm


def get_stop_loss(
    scrip,
    hist_data,
):
    """

    :param scrip:
    :param hist_data:
    :return:
    """
    price_SL = 0

    # On the basis of %age
    price_SL_percentage = 0

    # On the basis of PA
    price_SL_PA = 0

    # Determine a logic to set one of these values
    if price_SL_percentage < price_SL_PA:  # Mock logic
        price_SL = price_SL_percentage
    else:
        price_SL = price_SL_PA

    return price_SL


def get_target(scrip, hist_data):
    """

    :param scrip:
    :param hist_data:
    :return:
    """
    price_target = 0

    # On the basis of %age
    price_target_percentage = 0

    # On the basis of PA
    price_target_PA = 0

    # Determine a logic to set one of these values
    if price_target_percentage < price_target_PA:  # Mock logic
        price_target = price_target_percentage
    else:
        price_target = price_target_PA

    return price_target


def verify_entry_decision(scrip, hist_data):
    """

    :param scrip:
    :param hist_data:
    :return:
    """
    is_entry_valid = trade_algorithm.is_entry_valid(scrip, hist_data)
    # Any other checks that are out-of-scope for the Algo module
    return is_entry_valid


def take_entry(sorted_algo_output, hist_data):
    """

    :param sorted_algo_output:
    :param hist_data:
    :return:
    """
    for scrip in sorted_algo_output:
        # Step 1 : Runs Algo module to check if the trade still stands true, margin availability etc.
        if verify_entry_decision(scrip, hist_data):
            # Step 2 : Define SL
            get_stop_loss(scrip, hist_data)
            # set SL in some Kite function ??
            # Step 3 : Define Target
            get_target(scrip, hist_data)
            # set target in some kite function ??
            # Step 4 : Take entry
            # Invoke some Kite function probably ??
            active_trade_list = []
        else:
            exit()


# samplehistorical = open(v3_ConstantLib.SAMPLE_HISTORICAL, 'r').read()
