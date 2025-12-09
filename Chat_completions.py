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
        {"role": "system", "content": "You are a helpful AI agent."},
        {"role": "user", "content": "Could you generate 5 questions to interact with AI assistant based on some random theme on your choice (keep only sentencces without explanations, bulletpoints and numbers?"}
    ],
    temperature=0.1
)

questions = response.choices[0].message.content.split('\n')

#print(questions)

chat_output = []

for qusteion in questions:
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "You are an helpful assistant."},
            {"role": "user", "content": qusteion}
        ],
        temperature=0.1
    )
    chat_output.append(response.choices[0].message.content)
#print(response.choices[0].message.content)

for question, answer in zip(questions, chat_output):
    print()
    print(f"Question:\n{question}\n\nAnswer:\n{answer}")