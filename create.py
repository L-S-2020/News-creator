import requests, json, time, g4f, openai, ftfy
from urllib.parse import urlparse
from unsplash.api import Api
from unsplash.auth import Auth

SERVER = "http://127.0.0.1:8000/api/"
client_id = "KgSkM_iREcGUZA4PYUwPUmg1vFxLsiaNJkpWXGoXJnA"
client_secret = "31RTVz0Fk045ZBRklmJ-eAFwAIcO4kz8WBz8mNPK09U"
redirect_uri = ""
code = ""
openai.api_base = "https://neuroapi.host"
openai.api_key = "sk-6Z"
auth = Auth(client_id, client_secret, redirect_uri, code=code)
api = Api(auth)


def generate(prompt):
    g4f.logging = True  # enable logging
    g4f.check_version = False  # Disable automatic version checking
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    answer = response.choices[0].message.content
    return ftfy.fix_text(answer)

r = requests.get('https://newsdata.io/api/1/news?apikey=pub_2430005b32b1160236e845cf2ded9a93e1eb0&domainurl=tagesschau.de,merkur.de,www.faz.net,www.zeit.de,sueddeutsche.de')
response = json.loads(r.text)
print(response)
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

   prompt = f'''Schreibe den folgenden Artikel um, erfinde nichts hinzu, benutze Fesselnde und informative Sprache. Der neue Artikel muss mindesttens so lang wie der gegebene Artikel sein.
Benutze folgendes Layout:
Titel:
Beschreibung:
Inhalt:
Keywords:
Kategorie:
Bildtag:

Artikel:
Titel: {title}
Beschreibung: {description}
Inhalt: {content}
'''
   print(prompt)
   print(""
         "")
   try:
      output = generate(prompt)
   except:
      continue
   print(output)
   time.sleep(2)
   print("---------------------------------------------------")

   # Nehme Variabeln aus dem Output
   try:
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
      photo = api.search.photos(bildtags)
      print(photo['results'][0])
      url = photo['results'][0].links.download
      response = requests.get(url, allow_redirects=True)
      open('bild.jpg', 'wb').write(response.content)
   except:
      continue

   upload = requests.post(SERVER + "uploadArticle", data={"key": "123", "title": title, "description": beschreibung, "content": inhalt, "source": source, "url": url, "tags": keywords, "article_id": id}, files={"image": open("bild.jpg", "rb")})
   