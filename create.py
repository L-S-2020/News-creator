import requests, json, time, g4f
from urllib.parse import urlparse
from g4f.Provider import *

SERVER = "http://127.0.0.1:8000/api/"

def generate(prompt):
    g4f.logging = True  # enable logging
    g4f.check_version = False  # Disable automatic version checking
    antwort = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        provider=g4f.Provider.AItianhu
    )
    return antwort

r = requests.get('https://newsdata.io/api/1/news?apikey=pub_2430005b32b1160236e845cf2ded9a93e1eb0&country=de&prioritydomain=top')
response = json.loads(r.text)
results = response['results']
for i in results:
   title = i['title']
   url = i['link']
   source = urlparse(url).netloc
   description = i['description']
   content = i['content']
   content = content.lstrip(".")
   id = i['article_id']
   check = requests.post(SERVER + "checkNumber", data={"article_id": id})
   check = json.loads(check.text)
   if check["artikel"] == "existiert":
       continue

   prompt = f'''Schreibe den folgenden Artikel um, erfinde nichts hinzu, benutze Fesselnde und informative Sprache.
Benutze folgendes Layout:
Titel:
Beschreibung:
Inhalt:
Keywords:
Kategorie:

Artikel:
Titel: {title}
Beschreibung: {description}
Inhalt: {content}
'''
   print(prompt)
   print(""
         "")
   output = generate(prompt)
   print(output)
   time.sleep(2)
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


   upload = requests.post(SERVER + "uploadArticle", data={"key": "123", "title": title, "description": beschreibung, "content": inhalt, "source": source, "url": url, "tags": keywords, "article_id": id})
   