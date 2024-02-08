from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key= "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",
)

def generate(prompt):
    response = client.images.generate(
        model="dall-e-2",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    return image_url

image = generate("ein Foto von Kriese im Gazastreifen")
print(image)