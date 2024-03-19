import pandas as pd

ERSTELLEN_PROMPT = '''Schreibe einen Nachrichtenartikel aus folgender Zusammenfassung, erfinde nichts hinzu, benutze Fesselnde und informative Sprache. Der Inhalt muss mindestens 1000 Wörter lang sein!
Benutze folgendes Layout:
Titel:
Beschreibung:
Inhalt: 
Keywords:
Kategorie:
Bildtag:

Artikel:
Zusammenfassung: '''

df = pd.read_parquet("halluzinationen.parquet")
df = df[(df['Modell'] == 'gpt') | (df['Modell'] == 'mistral')]
# für jeden Artikel in der Tabelle, extraheire die Eingabe
for index, i in df.iterrows():
    eingabe = i['Eingabe']
    eingabe = eingabe.split(ERSTELLEN_PROMPT)[1]
    eingabe = eingabe.strip()
    df.at[index, 'Eingabe'] = eingabe
    gesamt = str(i['Gesamt'])
    gesamt = gesamt.split('Beschreibung')[0]
    gesamt = gesamt.strip()
    df.at[index, 'Gesamt'] = gesamt

df.to_excel("halluzinationen.xlsx")