from huggingface_hub import InferenceClient#
import newspaper
import requests, json

client = InferenceClient(
    "mistralai/Mistral-7B-Instruct-v0.1"
)

def format_prompt(message, history):
  prompt = "<s>"
  for user_prompt, bot_response in history:
    prompt += f"[INST] {user_prompt} [/INST]"
    prompt += f" {bot_response}</s> "
  prompt += f"[INST] {message} [/INST]"
  return prompt

def generate(
    prompt, history, temperature=0.9, max_new_tokens=256, top_p=0.95, repetition_penalty=1.0,
):
    temperature = float(temperature)
    if temperature < 1e-2:
        temperature = 1e-2
    top_p = float(top_p)

    generate_kwargs = dict(
        temperature=temperature,
        max_new_tokens=max_new_tokens,
        top_p=top_p,
        repetition_penalty=repetition_penalty,
        do_sample=True,
        seed=42,
    )

    formatted_prompt = format_prompt(prompt, history)

    stream = client.text_generation(formatted_prompt, **generate_kwargs, stream=True, details=True, return_full_text=False)
    output = ""

    for response in stream:
        output += response.token.text
        yield output
    return output

file = open("websites.txt")

#portal = newspaper.build('http://www.faz.net')
#print(portal)

#for article in portal.articles:
#    print(article.url)
#    article.download()
#    article.parse()
#    print(article.summary)

r = requests.get('https://newsdata.io/api/1/news?apikey=pub_2430005b32b1160236e845cf2ded9a93e1eb0&country=de')
response = json.loads(r.text)
print(response)
for i in response.results:
   article = json.loads(i)
   print(article.title)

