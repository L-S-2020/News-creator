# Module importieren
import time
import requests, json, ftfy, io, os
# OpenAI API
from openai import OpenAI
# Google News API
from gnews import GNews
# Huggingface Transformer
from transformers import pipeline
# Asynchrone Funktionen
import asyncio
# dotenv
from dotenv import load_dotenv
# Text
import textstat
# Pandas
import pandas as pd

load_dotenv()

ANZAHL_ARTIKEL = 300
Modal_API_KEY = os.getenv("Modal_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI API initialisieren
client = OpenAI(
    api_key= OPENAI_API_KEY,
)

# Variabeln initialisieren
kategorie = ""
keywords = ""
bildtags = ""
fehler = 0

textstat.set_lang('de')

# Erstelle Datenframe mit Spalten Modell, Eingabe, Ausgabe, Kategorie, Keywords, Bildtags, Textlänge, Flesch-Reading-Ease, Wienersachtextformel
#df = pd.DataFrame(columns=['Modell', 'Eingabe', 'Ausgabe', 'Text', 'Kategorie', 'Keywords', 'Bildtags', 'Textlänge', 'Flesch-Reading-Ease', 'Wienersachtextformel'])
df = pd.read_parquet("artikel.parquet")

print(df.info())

# Klassifizierungsmodell initialisieren bzw. herunterladen
pipe = pipeline("text-classification", model="lcrew/nachrichten-kategorisierer")

# Funktion zum Generieren von Texten mit OpenAI GPT-3.5
def generate_gpt(prompt):
   try:
      response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[{"role": "user", "content": prompt}],
      )
      answer = response.choices[0].message.content
      return ftfy.fix_text(answer)
   except:
      time.sleep(40)
      return 'Fehler'

# Funktion zum Generieren von Texten mit dem angepasssten, auf Mistral 7b basierenden Modell (in der Cloud)
def generate_mistral(prompt):
   response = requests.post('https://l-s-2020--example-vllm-inference-master.modal.run/', json={"question": prompt, "key": Modal_API_KEY}, allow_redirects=True)
   try:
      text = json.loads(response.text)
      return text['antwort']
   except:
      return 'Fehler'


# Eingaben: Zusammenfassung (Stichwörter des Artikels), URL (URL des Ausgangsartikels), Typ (GPT-3.5 oder Mistral)
async def artikel_generieren(zusammenfassung, url, type):
   # Variabeln global verfügbar machen, um sie außerhalb der Funktion zu verwenden
   global kategorie, keywords, bildtags, df, fehler

   # Artikel-ID, basierend auf URL und Modell generieren
   article_id = type + url

   # definiere Prompt, um den Artikel zu generieren
   prompt = f'''Schreibe einen Nachrichtenartikel aus folgender Zusammenfassung, erfinde nichts hinzu, benutze Fesselnde und informative Sprache. Der Inhalt muss mindestens 1000 Wörter lang sein!
Benutze folgendes Layout:
Titel:
Beschreibung:
Inhalt: 
Keywords:
Kategorie:
Bildtag:

Artikel:
Zusammenfassung: {zusammenfassung} '''

   # solange bis der Artikel korrekt generiert wurde
   falsch = True
   versuch = 0
   while falsch:
      # generiere Artikel aus Zusammenfassung
      if type == 'gpt':
         print('Generiere Artikel mit GPT-3.5')
         output = generate_gpt(prompt)
      if type == 'mistral':
         print('Generiere Artikel mit Mistral')
         output = generate_mistral(prompt)
         print(output)
         if output == 'Fehler':
            continue

      # überprüfe ob der Artikel korrekt generiert wurde
      try:
         # Nehme Variabeln aus dem Output
         titel = output
         titel = titel.split("Titel:")[1]
         titel = titel.split("Beschreibung:")[0]
         titel = titel.strip()
         beschreibung = output
         beschreibung = beschreibung.split("Beschreibung:")[1]
         beschreibung = beschreibung.split("Inhalt:")[0]
         beschreibung = beschreibung.strip()
         inhalt = output
         inhalt = inhalt.split("Inhalt:")[1]
         inhalt = inhalt.split("Keywords:")[0]
         inhalt = inhalt.strip()
         keywords = output
         keywords = keywords.split("Keywords:")[1]
         keywords = keywords.split("Kategorie:")[0]
         keywords = keywords.strip()
         bildtags = output
         bildtags = bildtags.split("Bildtag:")[1]
         bildtags = bildtags.strip()
         falsch = False
      except:
         versuch += 1
         if versuch > 5:
            versuch = 0
            falsch = False
            fehler += 1
            print("-------------Fehler-----------------")
            return
         continue


   # Ordne Artikel einer Kategorie zu, mithilfe des Klassifizierungsmodells
   kategorie = pipe(beschreibung)
   kategorie = kategorie[0]['label']

    # Textlänge, Flesch-Reading-Ease und Wienersachtextformel berechnen
   text = titel + ' ' + beschreibung + ' ' + inhalt
   textlänge = int(len(text.split()))
   flesch_index = textstat.flesch_reading_ease(text)
   wiener_index = textstat.wiener_sachtextformel(text, variant=1)

   # speichere Daten in Datenframe
   df = df._append({'Modell': type, 'Eingabe': prompt, 'Ausgabe': output, 'Text': text, 'Kategorie': kategorie,
            'Keywords': keywords, 'Bildtags': bildtags, 'Textlänge': textlänge, 'Flesch-Reading-Ease': flesch_index,
            'Wienersachtextformel': wiener_index}, ignore_index=True)

   print(type)
   print(output)
   print('--------')

   return

# generiere Artikel mit beiden Modellen gleichzeitig
async def run(zusammenfassung, url):
   await asyncio.gather(
      artikel_generieren(zusammenfassung, url, 'gpt'),
      artikel_generieren(zusammenfassung, url, 'mistral')
   )


# aktuelle Nachrichten von Google News holen
google_news = GNews(language='de', country='DE', period='90d', max_results=ANZAHL_ARTIKEL)
news = google_news.get_news('WORLD')

# für jeden Artikel
for i in news:
   # hole Artikelinhalt
   try:
      article = google_news.get_full_article(i['url'])
   except:
      continue

   # generiere Stichwortliste aus Artikelinhalt
   prompt = f'''Extrahiere die Informationen aus folgendem Artikel.
          Artikel: {article.text} '''
   zusammenfassung = generate_gpt(prompt)
   print('Artikel:' + i['title'])
   print(zusammenfassung)
   print()

   # Warte bis beide Artikel generiert wurden
   asyncio.run(run(zusammenfassung, i['url']))

   # speichere Artikel von menschlichem Schreiber
   text = i['title'] + ' ' + i['description'] + ' ' + article.text
   ausgabe = i['title'] + '\n' + i['description']
   textlänge = int(len(text.split()))
   flesch_index = textstat.flesch_reading_ease(text)
   wiener_index = textstat.wiener_sachtextformel(text, variant=1)
   df = df._append({'Modell': 'mensch', 'Eingabe': zusammenfassung, 'Ausgabe': ausgabe, 'Text': text, 'Kategorie': kategorie,
            'Keywords': keywords, 'Bildtags': bildtags, 'Textlänge': textlänge, 'Flesch-Reading-Ease': flesch_index,
            'Wienersachtextformel': wiener_index}, ignore_index=True)

   # speichere Datenframe
   df['Textlänge'] = df['Textlänge'].astype(str).astype(int)
   df.to_parquet("artikel.parquet")

# berechne Statistiken
print(df.describe())
print(df.info())
print(df.head())

print('Fehler: ', fehler)
