import pandas as pd
import os
from datetime import datetime
from dateutil import parser
from get_datasets import load_dictionary
from get_datasets import download_data

exemple_data = pd.read_csv("Data/FR0000003188.csv", index_col='Date')

def find_extreme_dates(directory):
    dates_list = []
    for filename in os.listdir(directory):
        with open(os.path.join("Data", filename), 'r') as datafile:
            date = parser.parse(datafile.readlines()[1][:10])
            dates_list.append(date)
    return str(min(dates_list))[:10], str(max(dates_list))[:10]

def momentum(old, actual):
    return 100*(actual - old)/old

def time_momentum(months, date):
    pass


def main(datadir):
    extremum_dates = find_extreme_dates(datadir)
    print(f"Les historiques de données récupérés sont entre {extremum_dates[0]} et {extremum_dates[1]}.")

if __name__ == '__main__':
    print(find_extreme_dates("Data"))
