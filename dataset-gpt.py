import requests, json, ftfy, time
from openai import OpenAI
import pandas as pd

#create a dataframe
df_old = pd.read_excel("news.xlsx")
df_new = pd.DataFrame(columns=['id', 'url', 'title-old', 'descripton-old', 'content-old', 'title-gpt', 'description-gpt', 'content-gpt','keywords-gpt','bildtags-gpt', 'article-gpt'])
#client = OpenAI(
#    api_key= "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",
#)
client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
def generate(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    answer = response.choices[0].message.content
    return ftfy.fix_text(answer)

for index, row in df_old.iterrows():
    richtig = False
    while richtig != True:
        try:
            title_old = row['title']
            description_old = row['description']
            content_old = row['content']
            id = row['id']
            url = row['url']
            prompt = f'''Schreibe den folgenden Artikel um, erfinde nichts hinzu, benutze Fesselnde und informative Sprache. Der neue Artikel muss mindesttens so lang wie der gegebene Artikel sein.
Benutze folgendes Layout:
Titel:
Beschreibung:
Inhalt:
Keywords:
Kategorie:
Bildtag:
                
Artikel:
Titel: {title_old}
Beschreibung: {description_old}
Inhalt: {content_old}
'''
            print(prompt)
            try:
                output = generate(prompt)
            except:
                print("-------------Fehler-OpenAI----------------")
                continue
            print(output)
            print("---------------------------------------------------")

            # Nehme Variabeln aus dem Output
            titel = output
            if "Title:" in titel:
                titel = titel.split("Title: ")[1]
            elif "TITEL:" in titel:
                titel = titel.split("TITEL: ")[1]
            else:
                titel = titel.split("Titel: ")[1]
            titel = titel.split("Beschreibung:")[0]
            titel = titel.strip()
            print(titel)
            beschreibung = output
            if "Bechreibung:" in beschreibung:
                beschreibung = beschreibung.split("Bechreibung:")[1]
            else:
                beschreibung = beschreibung.split("Beschreibung:")[1]
            beschreibung = beschreibung.split("Inhalt:")[0]
            beschreibung = beschreibung.strip()
            print(beschreibung)
            inhalt = output
            inhalt = inhalt.split("Inhalt:")[1]
            if "Keywords:" in inhalt:
                inhalt = inhalt.split("Keywords:")[0]
            inhalt = inhalt.strip()
            print(inhalt)
            artikel = titel + ' ' + beschreibung + ' ' + inhalt
        except Exception as ex:
            print("-------------Fehler----------------")
            continue
        try:
            df_new = df_new._append({'id': id, 'url': url, 'title-old': title_old, 'descripton-old': description_old, 'content-old': content_old, 'title-gpt': titel, 'description-gpt': beschreibung, 'content-gpt': inhalt, 'article-gpt': artikel}, ignore_index=True)
            df_new.to_excel("news-gpt.xlsx")
        except Exception as ex:
            print("-------------Fehler save!----------------")
            continue
        richtig = True
