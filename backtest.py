import pandas as pd
import yfinance as yf

def load_data(file):
    df = pd.read_csv(file)
    df_update = df[df["Code ISIN"].apply(lambda x: len(yf.Ticker(x).info)) > 3]
    print("Got", df_update.shape[0], "funds out of", df.shape[0])
    return df_update

def get_missing_funds(df):
    return [isin for isin in df[df["Yahoo query"].isna()]["Code ISIN"]]

def get_financial_data(df):
    pass
    
if __name__ == "__main__":
    df = load_data("dictionnary_isin_yahoo.csv")
    test_query = "LU1681044217"
    