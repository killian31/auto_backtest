import pandas as pd
import numpy as np
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import urllib3
import urllib.parse as urlparse
from urllib.parse import parse_qs
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pickle
from webdriver_manager.chrome import ChromeDriverManager


def save_cookie(driver, path):
    with open(path, 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)

def load_cookie(driver, path):
     with open(path, 'rb') as cookiesfile:
         cookies = pickle.load(cookiesfile)
         for cookie in cookies:
             driver.add_cookie(cookie)



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

def get_quote(symbol):
    msft = yfinance.Ticker(symbol)
    try:
        hist = msft.history(period="2d")
    except json.decoder.JSONDecodeError:
        return None
    try:
        hist.reset_index(inplace=True)
        jsdata = json.loads(hist.to_json())
        return jsdata["Close"]["0"]
    except (ValueError, KeyError) as e:
       return None


def web_lookup(isin):
    print(isin)
    # Search PyPI for Elemental.
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get("https://finance.yahoo.com/")
    load_cookie(browser, "tmp/cookie")
    time.sleep(5)
    search_bar = browser.find_element(By.XPATH, "//*[@id='yfin-usr-qry']").send_keys(isin)
    # browser.get_input(id="yfin-usr-qry").fill(isin)
    browser.find_element(By.XPATH, "//*[@id='header-desktop-search-button']']").click()

    time.sleep(5)

    parsed = urlparse.urlparse(browser.url)
    try:
        ticker = parse_qs(parsed.query)['p'][0]
        print('#'*100 + 'Found')
    except KeyError:
        ticker = "n/a"
        print('#'*100 + 'Not Found')
    browser.quit()
    return ticker

# df["Yahoo query"] = df["Code ISIN"].apply(web_lookup)

# df.to_csv("dictionnary_isin_yahoo.csv")

#driver = webdriver.Chrome(ChromeDriverManager().install())
#driver.get("https://finance.yahoo.com/")

# save_cookie(driver, 'tmp/cookie')

web_lookup("FR0000288946")