import requests, json, time, g4f
from g4f.Provider import *
def generate(prompt):
    g4f.logging = True  # enable logging
    g4f.check_version = False  # Disable automatic version checking
    antwort = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        provider=g4f.Provider.AItianhu,
    )
    return antwort

r = requests.get('https://newsdata.io/api/1/news?apikey=pub_2430005b32b1160236e845cf2ded9a93e1eb0&country=de')
response = json.loads(r.text)
results = response['results']
for i in results:
   title = i['title']
   url = i['link']
   description = i['description']
   content = i['content']
   content = content.lstrip(".")
   id = i['article_id']

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
   