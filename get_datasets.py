import pandas as pd
import yfinance as yf
from tqdm import tqdm

def load_dictionary(file):
    df = pd.read_csv(file)
    df_update = df.dropna(axis=0)
    print("Got", df_update.shape[0], "funds out of", df.shape[0])
    return df_update

def get_missing_funds(df):
    return [isin for isin in df[df["Yahoo query"].isna()]["Code ISIN"]]
    
def download_data(year_before, current_year, df):
        data = {}
        pbar = tqdm(total=df.shape[0])
        for isin in df["Code ISIN"]:
            pbar.update(1)
            hist = yf.Ticker(isin + ".PA").history(period="10y", debug=False)
            if list(hist.index) != []:
                print(int(str(hist.index[len(hist.index)-1])[:4]))
                if int(str(hist.index[0])[:4]) <= year_before and int(str(hist.index[len(hist.index)-1])[:4]) == current_year:
                    pbar.set_description("Isin code %s" % isin)
                    data[isin] = hist
                    hist.to_csv("Test/" + isin + ".csv")
            else:
                new_hist = yf.Ticker(isin).history(period="10y", debug=False)
                if list(new_hist.index) != []:
                    print(int(str(new_hist.index[len(new_hist.index)-1])[:4]))
                    if int(str(new_hist.index[0])[:4]) <= year_before and int(str(new_hist.index[len(new_hist.index)-1])[:4]) == current_year:
                        pbar.set_description("Isin code %s" % isin)
                        data[isin] = new_hist
                        new_hist.to_csv("Test/" + isin + ".csv")
        pbar.close()
        return data

if __name__ == "__main__":
    df = load_dictionary("dictionnary_isin_yahoo.csv")
    test_query = "FR0013048253"
     
    year_limit = 2015
    current_year = 2022
    data = download_data(year_limit, current_year, df)
    print(len(data), "unités de compte existantes entre" ,year_limit, "et", current_year)