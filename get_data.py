import pandas as pd
import numpy as np
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import urllib3

API_KEY = "Ls2TwN7ossKsGGznC4kV"

# Import des données

df_uc_darjeeling = pd.read_excel("listedarjeeling202001.xlsx")

# Preprocessing

## On s'intéresse seulement aux deux premières colonnes

df = df_uc_darjeeling.iloc[:, :2]

## Retrait des lignes d'en-tête)
df = df.dropna(axis=0)

def get_symbol_for_isin(isin):
    url = 'https://query1.finance.yahoo.com/v6/finance/search'
    print(isin)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36',
    }

    params = dict(
        q=isin,
        quotesCount=1,
        newsCount=0,
        listsCount=0,
        quotesQueryId='tss_match_phrase_query'
    )

    resp = requests.get(url=url, headers=headers, params=params)
    data = resp.json()
    if 'quotes' in data and len(data['quotes']) > 0:
        print('#'*100 + 'Found')
        return data['quotes'][0]['symbol']
    else:
        print('#'*100 + 'Not Found')
        return None

df["Yahoo query"] = df["Code ISIN"].apply(get_symbol_for_isin)

df.to_csv("dictionnary_isin_yahoo.csv")