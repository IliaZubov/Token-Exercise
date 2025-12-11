import os
from openai import AzureOpenAI

api_key = os.getenv("AZURE_API_KEY")
api_version = os.getenv("AZURE_API_VERSION")
azure_endpoint = os.getenv("R_AZURE_ENDPOINT")

client = AzureOpenAI(
    api_key=api_key,
    api_version="2025-03-01-preview",
    azure_endpoint=azure_endpoint
)

"""response = client.responses.create(
    model="gpt-4.1",
    input="Explain zero-trust security architecture"
)

print("Assistant: ", response.output_text)"""

resp1 = client.responses.create(
    model="gpt-4.1",
    input="Explain AzureOpenAPI responses"
)

print("Assistant: ", client.responses.retrieve(resp1.id).output_text)

resp2 = client.responses.create(
    model="gpt-4.1",
    input="Can you explain that in simple terms?",
    previous_response_id=resp1.id
)

print("Assistant: ", resp2.output_text)

client.responses.delete(resp1.id)

print("Assistant: ", client.responses.retrieve(resp1.id).output_text)
