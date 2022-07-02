import pandas as pd
import yfinance as yf
from tqdm import tqdm

def load_data(file):
    df = pd.read_csv(file)
    df_update = df.dropna(axis=0)
    print("Got", df_update.shape[0], "funds out of", df.shape[0])
    return df_update

def get_missing_funds(df):
    return [isin for isin in df[df["Yahoo query"].isna()]["Code ISIN"]]

def compute_momentum(date, months, data):
    pass
    


if __name__ == "__main__":
    df = load_data("dictionnary_isin_yahoo.csv")
    test_query = "LU0568621618"

    data = {}
    def test():
        for isin in tqdm(df["Code ISIN"]):
            print(isin)
            assert(str(yf.Ticker(isin).history(period="max").iloc[0,].name)[:10] == "2018-01-02")
        
    print(type(yf.Ticker(test_query).history(period="max")))
    #test()