import pandas as pd

# Import des données

df_uc_darjeeling = pd.read_excel("listedarjeeling202001.xlsx")
print(df_uc_darjeeling.head())
print(df_uc_darjeeling.shape)

# Preprocessing

## Retrait des lignes sans forme juridique (pour supprimer les lignes d'en-tête)

