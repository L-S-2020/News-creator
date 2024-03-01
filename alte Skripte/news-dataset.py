import requests, json
import pandas as pd

#create a dataframe
df = pd.read_excel("news.xlsx")
nextpage = 'oifo'

r = requests.get('https://newsdata.io/api/1/news?apikey=pub_2430005b32b1160236e845cf2ded9a93e1eb0&language=de&domainurl=tagesschau.de,merkur.de,www.faz.net,www.zeit.de,sueddeutsche.de')

while nextpage != '':
    response = json.loads(r.text)
    results = response['results']
    print(results)
    print(response)
    for i in results:
        title = i['title']
        description = i['description']
        content = i['content']
        content = content.lstrip(".")
        id = i['article_id']
        url = i['link']
        try:
            df = df._append({'id': id, 'title': title, 'description': description, 'content': content, 'url': url}, ignore_index=True)
            df.to_excel("news.xlsx")
            print("-------------save!----------------")
        except Exception as ex:
            print("-------------Fehler save!----------------")
            continue
    try:
        nextpage = response['nextPage']
    except:
        nextpage = ''
    r = requests.get('https://newsdata.io/api/1/news?apikey=pub_2430005b32b1160236e845cf2ded9a93e1eb0&language=de&page=' + nextpage)
