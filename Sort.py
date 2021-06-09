from operator import itemgetter, attrgetter

#TODO Integrate with Algo module

# algo_response = [{'tradingsymbol':'RELIANCE', 'action':'buy','sortvalue':321,'sorttype':'desc'}]
# A normalized response is expected from the algo module
algo_response = [
    {"instrument_token": 121345, "tradingsymbol": "3MINDIA", "sortvalue": 1000},
    {"instrument_token": 1147137, "tradingsymbol": "AARTIDRUGS", "sortvalue": 2000},
    {"instrument_token": 1793, "tradingsymbol": "AARTIIND", "sortvalue": 3000},
    {"instrument_token": 1378561, "tradingsymbol": "AAVAS", "sortvalue": -3000},
    {"instrument_token": 3329, "tradingsymbol": "ABB", "sortvalue": -5000}
]


def sort(algo_response):
    '''
    :param algo_response: contains the list of dictionaries to sort
    :return: a sorted list on the basis of the key "sortvalue"
    '''

    sorted_algo_response = sorted(algo_response,
                                  key=lambda k: k['sortvalue'],  # lambda argument:expression
                                  reverse=True)
    '''Both itemgetter() and lambda works but if performance is a concern, use operator.itemgetter() instead of 
    lambda as built-in functions perform faster than hand-crafted functions. '''
    # sorted_x = print(sorted(x, key=itemgetter('sortvalue')))
    print(sorted_algo_response)
    return sorted_algo_response


sort(algo_response)

#################################################################################################################

algo_response2 = [
    {"instrument_token": 121345, "tradingsymbol": "3MINDIA", "sort_value_1": 1000, "sort_value_2": 5000},
    {"instrument_token": 1147137, "tradingsymbol": "AARTIDRUGS", "sort_value_1": 2000, "sort_value_2": 4000},
    {"instrument_token": 1793, "tradingsymbol": "AARTIIND", "sort_value_1": 3000, "sort_value_2": 3000},
    {"instrument_token": 1378561, "tradingsymbol": "AAVAS", "sort_value_1": -3000, "sort_value_2": 2000},
    {"instrument_token": 3329, "tradingsymbol": "ABB", "sort_value_1": -5000, "sort_value_2": 1000}
]


def multisort(list_to_sort, criteria):
    '''
    This method can sort a list on the basis of multiple sorting keys. The priority of the keys is pre-defined
    and is stored in the criteria object.
    :param list_to_sort: self-explanatory
    :param criteria: Each element in the sorting_criteria object contains two values
                     Element 1 -> the actual sorting key
                     Element 2 -> boolean value to decide the order of sorting i.e. ascending or descending
    :return: a sorted list by iterating the criteria object
    '''
    for key, reverse in criteria:
        print(reverse)
        print(key)
        #To save the sorted list in a new object, use sorted()
        #sorted_list = sorted(list_to_sort.sort(key=itemgetter(key), reverse=reverse), key=itemgetter(key), reverse=reverse)
        list_to_sort.sort(key=itemgetter(key), reverse=reverse)
        print(list_to_sort)
    return list_to_sort

sorting_criteria = (('sort_value_1', False), ('sort_value_2', True))
multisort(algo_response2, sorting_criteria)

################  Obsolete methods. Delete this section in the final version   #############################

def sort_descending_order():
    list = [20, 5, -10, 300]
    list.sort(reverse=True)  # Sort the list in descending order
    print(list)
    return list


def sort_ascending_order():
    list = [200, 50, -100, 3000]
    list.sort()  # Sort the list in asscending order
    print(list)
    return list


def merge_sorted_lists():
    merged_list = sort_descending_order() + sort_ascending_order()
    print(merged_list)
    return merged_list

# merge_sorted_lists()
