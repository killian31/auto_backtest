import pandas as pd
import os
from datetime import datetime
from dateutil import parser
from dateutil import relativedelta
from get_datasets import load_dictionary
from get_datasets import download_data

exemple_data = pd.read_csv("Data/FR0000003188.csv", parse_dates=['Date'], index_col=['Date'])

def find_extreme_dates(directory):
    dates_list = []
    for filename in os.listdir(directory):
        with open(os.path.join("Data", filename), 'r') as datafile:
            try:
                date_str = datafile.readlines()[1][:10].strip()
            except UnicodeDecodeError:
                pass
            date = parser.parse(date_str)
            dates_list.append(date)
    return str(min(dates_list))[:10], str(max(dates_list))[:10]

def momentum(old, actual):
    return 100*(actual - old)/old

def time_momentum(months, date, df):
    old_value = df["Close"][date - relativedelta.relativedelta(months=months)]
    date_value = df["Close"][date]
    return momentum(old_value, date_value)


def main(datadir):
    extremum_dates = find_extreme_dates(datadir)
    print(f"Les données débutent entre {extremum_dates[0]} et {extremum_dates[1]}.")
    return None

if __name__ == '__main__':
    print(time_momentum(1, parser.parse(find_extreme_dates("Data")[1]), exemple_data))
