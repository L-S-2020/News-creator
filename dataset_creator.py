# Module importieren
import ftfy, os
# OpenAI API
from openai import OpenAI
# Google News API
from gnews import GNews

# Konstanten definieren
ANZAHL_ARTIKEL = 1

# OpenAI API initialisieren
client = OpenAI(
    api_key= os.environ.get("OPENAI_API_KEY"),
)

# Letzte Ausgabe einlesen
df = pd.read_excel("output.xlsx")

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
   zusammenfassung = generate(prompt)
   print('Artikel:' + i['title'])
   print(zusammenfassung)
   print()

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
Zusammenfassung: {zusammenfassung} '''

   output = f'''Titel: {i['title']}
Beschreibung: {i['description']}
Inhalt: {article.text}
Keywords: {i['keywords']}
Kategorie: {i['category']}
Bildtag: {i['image_tags']}'''

    # speichere Input und Output in Excel-Datei
   df = df.append({'input': input, 'output': output}, ignore_index=True)
   df.to_excel("output.xlsx")
   print("-------------save!----------------")


