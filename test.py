from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key= "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",
)
def generate(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    print(response)
    answer = response.choices[0].message.content
    return ftfy.fix_text(answer)

generate('Test')