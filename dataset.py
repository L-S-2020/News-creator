import requests, json, ftfy, time
from openai import OpenAI
import pandas as pd

#create a dataframe
df = pd.read_excel("output.xlsx")
nextpage = 'oifo'
client = OpenAI(
    # This is the default and can be omitted
    api_key= "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",
)
def generate(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    answer = response.choices[0].message.content
    return ftfy.fix_text(answer)

r = requests.get('https://newsdata.io/api/1/news?apikey=pub_2430005b32b1160236e845cf2ded9a93e1eb0&language=de')

while nextpage != '':
    response = json.loads(r.text)
    results = response['results']
    print(results)
    print(response)
    for i in results:
        richtig = False
        while richtig != True:
            try:
                title = i['title']
                description = i['description']
                content = i['content']
                content = content.lstrip(".")
                id = i['article_id']
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
                    print("-------------Fehler-OpenAI----------------")
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
                bildtags = output
                bildtags = bildtags.split("Bildtag:")[1]
                bildtags = bildtags.strip()
                print(bildtags)
            except Exception as ex:
                print("-------------Fehler----------------")
                time.sleep(20)
                continue
            try:
                df = df._append({'id': id, 'Prompt': prompt, 'output': output}, ignore_index=True)
                df.to_excel("output.xlsx")
            except Exception as ex:
                print("-------------Fehler save!----------------")
                continue
            richtig = True
    try:
        nextpage = response['nextPage']
    except:
        nextpage = ''
    r = requests.get('https://newsdata.io/api/1/news?apikey=pub_2430005b32b1160236e845cf2ded9a93e1eb0&language=de&page=' + nextpage)