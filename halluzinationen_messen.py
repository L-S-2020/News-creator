# Module importieren
import time
import requests, json, ftfy, io, os
# OpenAI API
from openai import OpenAI
# dotenv
from dotenv import load_dotenv
# Pandas
import pandas as pd

load_dotenv()

Modal_API_KEY = os.getenv("Modal_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

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

# OpenAI API initialisieren
client = OpenAI(
    api_key= OPENAI_API_KEY,
)

client2 = OpenAI(
    api_key= '',
)

client3 = OpenAI(
    api_key= '',
)

aktuell = 1
def generate_gpt(prompt):
    global aktuell
    generated = False
    while not generated:
        if aktuell == 1:
            ai = client
        if aktuell == 2:
            ai = client2
        if aktuell == 3:
            ai = client3
        try:
            response = ai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
            )
            generated = True
        except:
            aktuell += 1
            if aktuell == 4:
                aktuell = 1
    aktuell += 1
    if aktuell == 4:
        aktuell = 1
    answer = response.choices[0].message.content
    time.sleep(6)
    return ftfy.fix_text(answer)

df = pd.read_parquet("artikel.parquet")

df_ai = df[(df['Modell'] == 'gpt') | (df['Modell'] == 'mistral')]

for index, i in df_ai.iterrows():
    eingabe = i['Eingabe']
    notizen = eingabe.split(ERSTELLEN_PROMPT)
    notizen = notizen[1]
    artikel = i['Text']
    prompt = f'''Aus folgenden Notizen hat ein KI-Modell einen Nachrichtenartikel geschrieben:
    {notizen}

    Artikel:
    {artikel}


    Gib die Anzahl an hinzugefügten (halluzinierten) Informationen an, neben der Anzahl an, in den Notizen gegebenen und der gesamten, im Artikel enthaltenen. Schlussfolgerungen sind keine Fakten:
    Halluziniert:
    Gegeben:
    Gesamt:
    Beschreibung der halluzinierten Informationen:'''
    falsch = True
    while falsch:
        try:
            metriken = generate_gpt(prompt)
            print(metriken)
            halluziniert = metriken.split('Halluziniert:')[1]
            halluziniert = halluziniert.split('Gegeben:')[0]
            halluziniert = halluziniert.strip()
            urspruenglich = metriken.split('Gegeben:')[1]
            urspruenglich = urspruenglich.split('Gesamt:')[0]
            urspruenglich = urspruenglich.strip()
            gesamt = metriken.split('Gesamt:')[1]
            gesamt = gesamt.split('Beschreibung der Halluzinierten Informationen:')[0]
            gesamt = gesamt.strip()
            beschreibung = metriken.split('Beschreibung der halluzinierten Informationen:')[1]
            beschreibung = beschreibung.strip()
            print(halluziniert)
            print(urspruenglich)
            print(gesamt)
            print(beschreibung)
            print('--------------------------')
            df.at[index, 'Halluziniert'] = halluziniert
            df.at[index, 'Ursprünglich'] = urspruenglich
            df.at[index, 'Gesamt'] = gesamt
            df.at[index, 'Halluziniert-Beschreibung'] = beschreibung
            df.to_parquet("halluzinationen.parquet")
            falsch = False
            print('--------------------Index: ' + str(index) + '---------------------')
        except:
            print("-------------Fehler-----------------")

print(df)
