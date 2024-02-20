# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("text-classification", model="lcrew/autotrain-text")
output = pipe("Hackerangriff auf Microsoft")
print(output[0]['label'])
