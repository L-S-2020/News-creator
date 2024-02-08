from gnews import GNews
from openai import OpenAI
import ftfy

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
   return (ftfy.fix_text(answer))

google_news = GNews(language='de', country='DE', period='7d')
news = google_news.get_top_news()
for i in news:
    article = google_news.get_full_article(i['url'])
    prompt = f'''Fasse folgenden Artikel zusammen, lasse keine Informationen weg.
    Artikel: {article.text} '''
    zusammenfassung = generate(prompt)
    print(zusammenfassung)



