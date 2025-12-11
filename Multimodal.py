import os
from openai import AzureOpenAI
import base64

api_key = os.getenv("AZURE_API_KEY")
api_version = os.getenv("AZURE_API_VERSION")
azure_endpoint = os.getenv("R_AZURE_ENDPOINT")

client = AzureOpenAI(
    api_key=api_key,
    api_version="2025-03-01-preview",
    azure_endpoint=azure_endpoint
)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        base64_bytes = base64.b64encode(image_file.read())
        return base64_bytes.decode()
    
image_path = "C:/Users/IliaZubov/Documents/Skillio/week 8/Token Exercise/mango.jpeg"

base64_image = encode_image(image_path)

response = client.responses.create(
    model="gpt-4.1",
    input=[
        {"role":"user", "content": [
            {"type": "input_text", "text": "What kind a deserts can I make with this ingredient?"},
            {"type": "input_image", "image_url": f"data:image/jpeg;base64, {base64_image}"}
        ]}
    ]
)

retrieved = client.responses.retrieve(response.id)
print("Retrieved text:", retrieved.output_text)