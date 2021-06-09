import json
import os

import pandas as pandas

#TODO: Add methods to read/write .csv files and DataFrames, if required

'''
All the re-usable functions to be defined in this module.
This will limit code redundancy and improve readability.

References for OS package: https://automatetheboringstuff.com/chapter8/
'''


def read_file(file_name):
    '''
    File to-be-read is kept in a hard-coded '.../temp' directory
    :param file_name: to be provided by the module that invokes this funciton
    :return: data that might be either of the list or dictionary collection types
    '''
    directory = get_directory()
    file_path = os.path.join(directory, file_name + ".txt")
    with open(file_path, "r") as file:
        read_file = json.load(file)
    return read_file


def write_file(data, file_name, append):
    '''
    :param data: might be either of the list or dictionary collection types
    :param file_name: to be provided explicitly for each module where this function is invoked. Ex: stocklist.txt, historicalData.txt
    :param append: boolean 'True' if new data is to be appended to the existing data, else boolean 'False'
    :return: nothing but creates the directory '.../temp' (not to be committed) where the file_name is then created.
             Stores the argument 'data' in the created file_name for the current session.
    '''
    directory = get_directory()
    file_path = os.path.join(directory, file_name + ".txt")
    print(file_path)
    print(os.getcwd())
    if append and os.path.isfile(file_path):
        with open(file_path, "r+") as file:  # With mode set as "r+" -> open filename for reading and writing
            existing_data = json.load(file)
            if isinstance(data, dict):
                existing_data.update(data)
            elif isinstance(data, list):
                existing_data.append(data)
            file.seek(0)  # Resets the file pointer to position 0
            json.dump(existing_data, file)
    else:
        with open(file_path, "w") as file:  # With mode set as "w" -> open filename for writing
            json.dump(data, file)


def get_directory():
    # abs_directory = "C:\Users\Suyash Kumar Rai\Documents"+"\\"+filename+".txt" # To set an absolute pre-defined path
    # directory = os.path.expanduser('~') # Finds relative path of the user's home directory
    current_directory = os.getcwd()  # Gets the current directory's path where the TradingBot project is located
    directory_path = os.path.join(current_directory, 'temp')
    if (os.path.isdir(directory_path)):
        exit
    else:
        os.makedirs(directory_path)

    return directory_path


#####################################   Test Data. Delete in the final version.    ###################################################

data_list = [
    {"instrument_token": 121345, "tradingsymbol": "3MINDIA", "sortvalue": 1000},
    {"instrument_token": 1147137, "tradingsymbol": "AARTIDRUGS", "sortvalue": 2000},
    {"instrument_token": 1793, "tradingsymbol": "AARTIIND", "sortvalue": 3000},
    {"instrument_token": 1378561, "tradingsymbol": "AAVAS", "sortvalue": -3000},
    {"instrument_token": 3329, "tradingsymbol": "ABB", "sortvalue": -5000}
]
data_dict = {
    "status4": "success",
    "data4": {
        "candles4": [
            ["2015-12-28T09:15:00+0530", 1386.4, 1388, 1381.05, 1385.1, 788],
            ["2015-12-28T09:16:00+0530", 1385.1, 1389.1, 1383.85, 1385.5, 609],
            ["2015-12-28T09:17:00+0530", 1385.5, 1387, 1385.5, 1385.7, 212],
            ["2015-12-28T09:18:00+0530", 1387, 1387.95, 1385.3, 1387.95, 1208],
            ["2015-12-28T09:19:00+0530", 1387, 1387.55, 1385.6, 1386.25, 716],
            ["2015-12-28T09:20:00+0530", 1386.95, 1389.95, 1386.95, 1389, 727]
        ]
    }
}
write_file(data_list, "test_list", True)
read_file("test_list")
write_file(data_dict, "test_dict", True)
read_file("test_dict")

nifty500 = pandas.read_csv("https://www1.nseindia.com/content/indices/ind_nifty500list.csv")
nifty_list = []
i = 0
while i < nifty500['Symbol'].size:
    nifty_list.append({"instrument_token": nifty500['ISIN Code'].get(i), "tradingsymbol": nifty500['Symbol'].get(i)})
    i += 1
write_file(nifty_list, "scrip_list", False)
read_file("scrip_list")