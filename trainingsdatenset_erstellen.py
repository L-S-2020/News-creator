# Module importieren
import ftfy, os
# OpenAI API
from openai import OpenAI
# Google News API
from gnews import GNews
# Pandas
import pandas as pd
# Huggingface Transformer
from transformers import pipeline
# dotenv
from dotenv import load_dotenv

load_dotenv()

# Konstanten definieren
ANZAHL_ARTIKEL = 1000 # Anzahl der Artikel, die von Google News geholt werden sollen

# OpenAI API initialisieren
client = OpenAI(
    api_key= os.environ.get("OPENAI_API_KEY"),
)

# Letzte Ausgabe einlesen, falls vorhanden, sonst leeres DataFrame erstellen
try:
   df = pd.read_excel("output.xlsx")
except:
   df = pd.DataFrame(columns=['input', 'output'])

# Klassifizierungsmodell initialisieren bzw. herunterladen
pipe = pipeline("text-classification", model="lcrew/nachrichten-kategorisierer")

# Funktion zum Generieren von Texten mit OpenAI GPT-3.5
def generate(prompt):
   response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[{"role": "user", "content": prompt}],
   )
   answer = response.choices[0].message.content
   return ftfy.fix_text(answer)


# aktuelle Nachrichten von Google News holen
google_news = GNews(language='de', country='DE', period='7d', max_results=ANZAHL_ARTIKEL)
news = google_news.get_top_news()

# für jeden Artikel
for i in news:
   # hole Artikelinhalt
   article = google_news.get_full_article(i['url'])

   # generiere Stichwortliste aus Artikelinhalt
   prompt = f'''Extrahiere die Informationen aus folgendem Artikel.
          Artikel: {article.text} '''
   stichworte = generate(prompt)
   print('Artikel:' + i['title'])
   print(stichworte)
   print()

   # Extrahiere Keywords
   article.nlp()
   keywords = article.keywords

   # Bestimme Kategorie mit Klassifizierungsmodell
   Kategorie = pipe(i['description'])[0]['label']

   # Generiere Bildtag aus Keywords mit GPT-3.5
   prompt = f'''Generiere einen Bildtag aus folgenden Keywords.
            Keywords: {keywords} 
            Bildtag: '''
   bildtag = generate(prompt)

   # Definiere Input und Output
   input = f'''Schreibe einen Nachrichtenartikel aus folgender Zusammenfassung, erfinde nichts hinzu, benutze Fesselnde und informative Sprache. Der Inhalt muss mindestens 1000 Wörter lang sein!
Benutze folgendes Layout:
Titel:
Beschreibung:
Inhalt: mindestens 1000 Wörter!
Keywords:
Kategorie:
Bildtag:

Artikel:
Zusammenfassung: {stichworte} '''

   output = f'''Titel: {i['title']}
Beschreibung: {i['description']}
Inhalt: {article.text}
Keywords: {keywords}
Kategorie: {Kategorie}
Bildtag: {bildtag}'''

    # speichere Input und Output in Excel-Datei
   df = df._append({'input': input, 'output': output}, ignore_index=True)
   df.to_excel("output.xlsx")
   print("-------------save!----------------")


