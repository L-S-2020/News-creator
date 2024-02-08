import requests, json, ftfy
from urllib.parse import urlparse
from translate import Translator
from unsplash.api import Api
from unsplash.auth import Auth
from openai import OpenAI
from gnews import GNews
from test_image import bild

translator= Translator(to_lang="en")

SERVER = "http://127.0.0.1:8000/api/"
client_id = "KgSkM_iREcGUZA4PYUwPUmg1vFxLsiaNJkpWXGoXJnA"
client_secret = "31RTVz0Fk045ZBRklmJ-eAFwAIcO4kz8WBz8mNPK09U"
redirect_uri = ""
code = ""
client = OpenAI(
    # This is the default and can be omitted
    api_key= "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",
)
auth = Auth(client_id, client_secret, redirect_uri, code=code)
api = Api(auth)

def sucheBild(bildtags):
   #setze Header
   header = {'Authorization': 'Bearer v2/aVUwYmtza2NwaDUwdnFOcjdnZnlJMHhHTzJsTWtlZjkvNDE5ODEyNTMxL2N1c3RvbWVyLzQvcl9oeDQ3YW1uQXN4cXRRVDJZRzB1NnljSy1hQVBOd280TG1YNTNYSmJfN0hpcDRkYXdtS0MwWkVCN3RISC1WWWMyaHUzOEJ6bloxMXRfcXhUZDFiT1hNNGVtSWJEMGlWc2Q0NHJBMXpwaWFGOFZQcmY3d1BvdlprYk5jNk9LcGZncERVUHRxR25VMlpaenJ3N0Y2UXdYbjBKUjF3czdJem1QSVFXTmJrX09IY19wS19la2ZMM2k2cFNiYTR5NlNjQU54akwycEhBajlnZDV2bkpfVG5Zdy81TzZLc1hfX29Fd2d5bXlFbG1CQWNn'}
   response = requests.get("https://api.shutterstock.com/v2/images/search?query=" + bildtags + "&image_type=photo&orientation=horizontal", headers=header)
   response = json.loads(response.text)
   response = response['data']
   if response[0]['assets']['preview_1500']['url'] != None:
      return (response[0]['assets']['preview_1500']['url'])
   else:
      photo = api.search.photos(bildtags)
      print(photo['results'][0])
      url = photo['results'][0].links.download
      return url


def generate(prompt):
   response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[{"role": "user", "content": prompt}],
   )
   answer = response.choices[0].message.content
   return ftfy.fix_text(answer)

google_news = GNews(language='de', country='DE', period='7d', max_results=1)
news = google_news.get_top_news()
for i in news:
   article = google_news.get_full_article(i['url'])
   check = requests.post(SERVER + "checkNumber", data={"article_id": i['url']})
   check = json.loads(check.text)
   if check["artikel"] == "existiert":
       continue
   prompt = f'''Fasse folgenden Artikel zusammen, lasse keine Informationen weg.
       Artikel: {article.text} '''
   zusammenfassung = generate(prompt)

   prompt = f'''Schreibe einen Nachrichtenartikel aus folgender Zusammenfassung, erfinde nichts hinzu, benutze Fesselnde und informative Sprache. Der Artikel sollte mindestens 200 Wörter lang sein.
Benutze folgendes Layout:
Titel:
Beschreibung:
Inhalt:
Keywords:
Kategorie:
Bildtag:

Artikel:
Zusammenfassung: {zusammenfassung} '''
   print(prompt)
   print(""
         "")
   try:
      output = generate(prompt)
   except:
      continue
   print(output)
   print("---------------------------------------------------")

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
   kategorie = output
   kategorie = kategorie.split("Kategorie:")[1]
   kategorie = kategorie.split("Bildtag:")[0]
   kategorie = kategorie.strip()
   print(kategorie)
   bildtags = output
   bildtags = bildtags.split("Bildtag:")[1]
   bildtags = bildtags.strip()
   print(bildtags)
   bild(bildtags)

   upload = requests.post(SERVER + "uploadArticle", data={"key": "123", "title": titel, "description": beschreibung, "content": inhalt, "source": 'Google News', "url": i['url'], "tags": keywords, "article_id": i['url'], 'art': 'gpt'}, files={"image": open("bild.png", "rb")})