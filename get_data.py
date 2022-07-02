import pandas as pd
import requests
from tqdm import tqdm


API_KEY = "2a2a8d02-0351-47a6-9111-1bd9011f39fe"

# Import des données

df_uc_darjeeling = pd.read_excel("listedarjeeling202001.xlsx")

# Preprocessing

## On s'intéresse seulement aux deux premières colonnes

df = df_uc_darjeeling.iloc[:, :2]

## Retrait des lignes d'en-tête)
df = df.dropna(axis=0)

pbar = tqdm(total = df.shape[0])

def isin_to_symbol(isin):
    global pbar
    global API_KEY
    # print(isin)
    url = 'https://api.openfigi.com/v3/mapping'
    headers = {'Content-Type':'text/json', 'X-OPENFIGI-APIKEY':f'{API_KEY}' }
    payload = '[{"idType":"ID_ISIN","idValue":' + f'"{isin}"' + '}]'
    r = requests.post(url, headers=headers, data=payload)
    pbar.set_description("Isin code %s" % isin)
    pbar.update(1)
    if r.status_code == 200:
        json_response = r.json()
        if 'data' in json_response[0].keys():
            return json_response[0]['data'][0]['ticker']
        else:
            return ""
    else:
        return ""

def create_data():
    df["Yahoo query"] = df["Code ISIN"].apply(lambda x: isin_to_symbol(x))
    df.to_csv("dictionnary_isin_yahoo.csv")

if __name__ == "__main__":
    create_data()
    pbar.close()
