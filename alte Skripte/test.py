import pandas as pd
import ftfy

#create a dataframe
df = pd.read_excel("output.xlsx")

file = open("trainingsdatenset.jsonl", "w", encoding="utf-8")

for index, row in df.iterrows():
    p =  '/n'.join(row["Prompt"].splitlines())
    o =  '/n'.join(row["output"].splitlines())
    # replace " with '
    p = p.replace('"', "'")
    o = o.replace('"', "'")
    file.write('{"instruction": "' + p + '", "output": "' + o + '"}\n')


prompt = f'''Schreibe einen vollständigen Artikel aus folgender Beschreibung, erfinde nichts hinzu, benutze Fesselnde und informative Sprache.
Benutze folgendes Layout:
Titel:
Beschreibung:
Inhalt:
Keywords:
Kategorie:
Bildtag:

Beschreibung:
{content}
'''




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


def generate(prompt):
   response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[{"role": "user", "content": prompt}],
   )
   answer = response.choices[0].message.content
   return (ftfy.fix_text(answer))

# holen Artikelbeschreibungen von Newsdata.io
r = requests.get('https://newsdata.io/api/1/news?apikey=iurffhfkjhkfhufiuh8iiruj&domainurl=tagesschau.de,merkur.de,www.faz.net,www.zeit.de,sueddeutsche.de')
response = json.loads(r.text)
results = response['results']
for i in results:
    # nehme Variabeln aus dem JSON
   url = i['link']
   source = urlparse(url).netloc
   content = i['description']
   id = i['article_id']
   # überprüfe ob Artikel schon existiert
   check = requests.post(SERVER + "checkNumber", data={"article_id": id})
   check = json.loads(check.text)
   if check["artikel"] == "existiert":
       continue
   try:
        # generiere Artikel aus Beschreibung
      output = generate(prompt)
   except:
      continue

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
      kategorie = output
      kategorie = kategorie.split("Kategorie:")[1]
      kategorie = kategorie.split("Bildtag:")[0]
      kategorie = kategorie.strip()
      print(kategorie)
      bildtags = output
      bildtags = bildtags.split("Bildtag:")[1]
      bildtags = bildtags.strip()
      # übersetze Bildtags ins Englische (für Unsplash)
      bildtags_t = translator.translate(bildtags)
      print(bildtags_t)
      # suche Bild auf Unsplash
      photo = api.search.photos(bildtags_t)
      print(photo['results'][0])
      url = photo['results'][0].links.download
      # lade Bild herunter
      response = requests.get(url, allow_redirects=True)
      open('../bild.jpg', 'wb').write(response.content)
   except:
      continue
    # lade Artikel hoch
   upload = requests.post(SERVER + "uploadArticle", data={"key": "123", "title": title, "description": beschreibung, "content": inhalt, "source": source, "url": url, "tags": keywords, "article_id": id}, files={"image": open(
      "../bild.jpg", "rb")})