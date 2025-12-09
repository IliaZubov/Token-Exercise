import tiktoken
import os
from openai import AzureOpenAI
from typing import List, Dict

api_key = os.getenv("AZURE_API_KEY")
api_version = os.getenv("AZURE_API_VERSION")
azure_endpoint = os.getenv("AZURE_ENDPOINT")

client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=azure_endpoint
)

def num_tokens_from_messages(messages: List[Dict[str,str]], model: str = "gpt-4.1") -> int:
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    
    if "gpt-3.5" in model:
        tokens_per_message = 4  # every message has <im_start>{role/name}\n{content}<im_end>\n
        tokens_per_name = -1    # if name is present, role is omitted
    elif "gpt-4" in model:
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(f"Token counting not implemented for model {model}")
    
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3
    return num_tokens

if __name__ == "__main__":
    
    chat_history = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "I'm doing well, thank you! How can I help you today?"},
        {"role": "user", "content": "Can you summarize our conversation so far?"}
    ]

    model_name = "gpt-4.1"  # Azure OpenAI model name
    token_count = num_tokens_from_messages(chat_history, model=model_name)

    print(f"Token count for chat history: {token_count}")
            

"""response = client.chat.completions.create(
    model="gpt-4.1", 
    messages=[
        {"role": "system", "content": "You are a helpful AI agent."},
        {"role": "user", "content": "Could you generate 5 questions to interact with AI assistant based on some random theme on your choice (keep only sentencces without explanations, bulletpoints and numbers?"}
    ],
    temperature=0.1
)

questions = response.choices[0].message.content.split('\n')

chat_output = []

for question in questions:
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "You are an helpful assistant."},
            {"role": "user", "content": question}
        ],
        temperature=0.1
    )
    chat_output.append(response.choices[0].message.content)
#print(response.choices[0].message.content)

for question, answer in zip(questions, chat_output):
    print()
    print(f"Question:\n{question}\n\nAnswer:\n{answer}")"""