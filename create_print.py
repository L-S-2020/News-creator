# Module importieren
import requests, json, ftfy, io, os
# OpenAI API
from openai import OpenAI
# Google News API
from gnews import GNews
# Bildgenerierung
from PIL import Image
# Huggingface Transformer
from transformers import pipeline
# Asynchrone Funktionen
import asyncio

# Konstanten definieren
SERVER = "http://127.0.0.1:8000/api/"
STABLE_DIFFUSION_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
STABLE_DIFFUSION_HEADERS = {"Authorization": os.environ.get("HF_API_KEY")}
ANZAHL_ARTIKEL = 1
SERVER_API_KEY = os.environ.get("SERVER_API_KEY")

# OpenAI API initialisieren
client = OpenAI(
    api_key= os.environ.get("OPENAI_API_KEY"),
)

# Variabeln initialisieren
kategorie = ""
keywords = ""

# Klassifizierungsmodell initialisieren bzw. herunterladen
pipe = pipeline("text-classification", model="lcrew/nachrichten-kategorisierer")

# Funktion zum Generieren von Texten mit OpenAI GPT-3.5
def generate_gpt(prompt):
   response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[{"role": "user", "content": prompt}],
   )
   answer = response.choices[0].message.content
   return ftfy.fix_text(answer)

# Funktion zum Generieren von Texten mit dem angepasssten, auf Mistral 7b basierenden Modell
def generate_mistral(prompt):
   response = requests.post('https://l-s-2020--example-vllm-inference-master-dev.modal.run/', json={"question": prompt, "key": os.environ.get('Modal_API_KEY')}, allow_redirects=True)
   text = json.loads(response.text)
   return text['antwort']

# Funktion zum Generieren von Bildern mithilfe von Bildtags
def bild(tags):
    # Bildtags in Prompt einfügen
    eingabe = f'''Ein Foto von {tags}, fotorealistisch'''
    daten = {"inputs": eingabe}
    # Anfrage an API
    response = requests.post(STABLE_DIFFUSION_API_URL, headers=STABLE_DIFFUSION_HEADERS, json=daten)
    image_bytes = response.content
    # Bild speichern
    image = Image.open(io.BytesIO(image_bytes))
    image.save("bild.png")

# Asynchrone Funktion zum Generieren und Hochladen von Artikeln
# Eingaben: Zusammenfassung (Stichwörter des Artikels), URL (URL des Ausgangsartikels), Typ (GPT-3.5 oder Mistral)
async def artikel_generieren(zusammenfassung, url, type):
   # Variabeln global verfügbar machen, um sie außerhalb der Funktion zu verwenden
   global kategorie, keywords

   # Artikel-ID, basierend auf URL und Modell generieren
   article_id = type + url

   # überprüfen ob Artikel schon existiert
   check = requests.post(SERVER + "checkNumber", data={"article_id": article_id})
   check = json.loads(check.text)
   if check["artikel"] == "existiert":
      return

   # definiere Prompt, um den Artikel zu generieren
   prompt = f'''Schreibe einen Nachrichtenartikel aus folgender Zusammenfassung, erfinde nichts hinzu, benutze Fesselnde und informative Sprache. Der Inhalt muss mindestens 1000 Wörter lang sein!
Benutze folgendes Layout:
Titel:
Beschreibung:
Inhalt: mindestens 1000 Wörter!
Keywords:
Kategorie:
Bildtag:

Artikel:
Zusammenfassung: {zusammenfassung} '''

   # solange bis der Artikel korrekt generiert wurde
   falsch = True
   while falsch:
      # generiere Artikel aus Zusammenfassung
      if type == 'gpt':
         print('Generiere Artikel mit GPT-3.5')
         output = generate_gpt(prompt)
      if type == 'mistral':
         print('Generiere Artikel mit Mistral')
         output = generate_mistral(prompt)

      # überprüfe ob der Artikel korrekt generiert wurde
      try:
         # Nehme Variabeln aus dem Output
         titel = output
         titel = titel.split("Titel: ")[1]
         titel = titel.split("Beschreibung:")[0]
         titel = titel.strip()
         print(titel)
         beschreibung = output
         beschreibung = beschreibung.split("Beschreibung:")[1]
         beschreibung = beschreibung.split("Inhalt:")[0]
         beschreibung = beschreibung.strip()
         print(beschreibung)
         inhalt = output
         inhalt = inhalt.split("Inhalt:")[1]
         inhalt = inhalt.split("Keywords:")[0]
         inhalt = inhalt.strip()
         print(inhalt)
         keywords = output
         keywords = keywords.split("Keywords:")[1]
         keywords = keywords.split("Kategorie:")[0]
         keywords = keywords.strip()
         print(keywords)
         bildtags = output
         bildtags = bildtags.split("Bildtag:")[1]
         bildtags = bildtags.strip()
         print(bildtags)
         falsch = False
      except:
         continue


   # Ordne Artikel einer Kategorie zu, mithilfe des Klassifizierungsmodells
   kategorie = pipe(beschreibung)
   kategorie = kategorie[0]['label']
   print(kategorie)

   # generiere Bild mithilfe von Bildtags
   bild(bildtags)

   # lade Artikel auf den Server
   upload = requests.post(SERVER + "uploadArticle", data={"key": SERVER_API_KEY, "title": titel, "description": beschreibung, "content": inhalt,"kategorie": kategorie, "source": 'Google News', "url": i['url'], "tags": keywords, "article_id": article_id, 'art': type}, files={"image": open("bild.png", "rb")})
   return

# generiere Artikel mit beiden Modellen gleichzeitig
async def run(zusammenfassung, url):
   await asyncio.gather(
      artikel_generieren(zusammenfassung, url, 'gpt'),
      artikel_generieren(zusammenfassung, url, 'mistral')
   )


# aktuelle Nachrichten von Google News holen
google_news = GNews(language='de', country='DE', period='7d', max_results=ANZAHL_ARTIKEL)
news = google_news.get_news('BUSINESS')

# für jeden Artikel
for i in news:
   # hole Artikelinhalt
   article = google_news.get_full_article(i['url'])

   # überprüfe ob Artikel schon existiert
   check = requests.post(SERVER + "checkNumber", data={"article_id": 'gpt' + i['url']})
   check = json.loads(check.text)
   if check["artikel"] == "existiert":
      print('Artikel existiert schon')
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

   # lade den originalen Artikel auf den Server
   upload = requests.post(SERVER + "uploadArticle",
                          data={"key": SERVER_API_KEY, "title": i['title'], "description": i['description'], "content": article.text,
                                "kategorie": kategorie, "source": 'Google News', "url": i['url'], "tags": keywords,
                                "article_id": 'mensch' + i['url'], 'art': 'mensch'}, files={"image": open("bild.png", "rb")})
