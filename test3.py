from gnews import GNews
import pandas as pd

articles = {}
topics = ['WORLD', 'NATION', 'BUSINESS', 'TECHNOLOGY', 'ENTERTAINMENT', 'SPORTS', 'SCIENCE', 'HEALTH']

google_news = GNews(language='de', country='DE')

for t in topics:
    news = google_news.get_news_by_topic(t)
    for i in news:
        article = google_news.get_full_article(i['url'])
        try:
            articles[article.text] = t
        except:
            print('next')
    print(len(articles))
    data = pd.DataFrame.from_dict(articles,orient='index')
    data.to_csv('classification.csv')



