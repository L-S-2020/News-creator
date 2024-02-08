import requests
import io
from PIL import Image
def bild(tags):
	API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
	headers = {"Authorization": "Bearer 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"}
	prompt = f'''Ein Foto von {tags}, fotorealistisch'''
	def query(payload):
		response = requests.post(API_URL, headers=headers, json=payload)
		return response.content
	image_bytes = query({
		"inputs": prompt,
	})
	image = Image.open(io.BytesIO(image_bytes))
	image.save("bild.png")