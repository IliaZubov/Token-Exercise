import os
from openai import AzureOpenAI

api_key = os.getenv("AZURE_API_KEY")
api_version = os.getenv("AZURE_API_VERSION")
azure_endpoint = os.getenv("AZURE_ENDPOINT")

client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=azure_endpoint
)

response = client.chat.completions.create(
    model="gpt-4.1", 
    messages=[
        {"role": "system", "content": "You are a historical expert."},
        {"role": "user", "content": "Why exactly is the sinking of Titanic such a big deal?"}
    ],
    temperature=0.1
)
print("response1:")
print(response.choices[0].message.content)

response2 = client.chat.completions.create(
    model="gpt-4.1", 
    messages=[
        {"role": "system", "content": "You are a journalist in 1912 in The New York Times."},
        {"role": "user", "content": "Why exactly is the sinking of Titanic such a big deal?"}
    ],
    temperature=0.8
)
print("response2:")
print(response2.choices[0].message.content)

response3 = client.chat.completions.create(
    model="gpt-4.1", 
    messages=[
        {"role": "system", "content": "You are the one of the passengers who survived in Titanic disaster."},
        {"role": "user", "content": "Why exactly is the sinking of Titanic such a big deal?"}
    ],
    temperature=0.5
)
print("response3:")
print(response3.choices[0].message.content)