# Pandas
import pandas as pd
import requests

SERVER = ""

# Erstelle Datenframe mit Spalten Modell, Eingabe, Ausgabe, Kategorie, Keywords, Bildtags, Textlänge, Flesch-Reading-Ease, Wienersachtextformel
df = pd.DataFrame(columns=['Sterne', 'art', 'kategorie', 'identifiziert', 'richtig', 'artikel',])

response = requests.get(SERVER + '/api/getbewertungen')
dictionary = response.json()
liste = dictionary['bewertungen']
for i in liste:
    df = df._append({'Sterne': i['sterne'], 'art': i['art'], 'kategorie': i['kategorie'], 'identifiziert': i['identifiziert'], 'richtig': i['richtig'], 'artikel': i['artikel']}, ignore_index=True)


print(df.info())
print(df.head())
print(df.describe())

df.to_parquet("bewertungen.parquet")