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

messages = [
    {"type": "message", "role": "system", "content": "You are a bike mechanic expert."}
]
    
while True:
    user_input = input("Question: ")

    if user_input.lower() in ["exit", "quit"]:
        break

    messages.append({"type": "message", "role": "user", "content": user_input})
    
    response = client.responses.create(
        model="gpt-4.1",
        input=messages
    )
    
    #messages.append(client.responses.retrieve(response.id).output_text)
    
    assistant_text = client.responses.retrieve(response.id).output_text
    
    messages.append({
        "type": "message",
        "role": "assistant",
        "content": assistant_text
    })
    
    print("Answer: ", client.responses.retrieve(response.id).output_text)
    