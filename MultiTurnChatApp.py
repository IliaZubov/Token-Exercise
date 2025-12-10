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

messages = [
    {"role": "system", "content": "You are a bike mechanic expert."}
]

while True:
    user_input = input("Question: ")
    
    if user_input.lower() in ["exit", "quit"]:
        break

    messages.append({"role": "user", "content": user_input})
    
    assistant_reply = ""
    
    while True:

        response = client.chat.completions.create(
            model="gpt-4.1", 
            messages=messages,
            temperature=0.1,
            max_tokens=100
        )
        
        chunk = response.choices[0].message.content
        
        assistant_reply += chunk
        
        if response.choices[0].finish_reason != "length":
            break
        
        messages.append({"role": "assistant", "content": chunk})
                
        messages.append({"role": "user", "content": "Please provide a shorter/summary response."})
        
    messages.append({"role": "assistant", "content": assistant_reply})
    
    print("\nAnswer:", assistant_reply, "\n")    
        
