import os
from openai import AzureOpenAI
import time
import tiktoken
import json

api_key = os.getenv("AZURE_API_KEY")
api_version = os.getenv("AZURE_API_VERSION")
azure_endpoint = os.getenv("AZURE_ENDPOINT")

client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=azure_endpoint
)

encoding = tiktoken.encoding_for_model("gpt-4.1")

messages = [
    {"role": "system", "content": "You are a FBI detective"}
]

TOKEN_WARNING_LIMIT = 1000

usage = None

def estimate_cost(prompt_tokens, completion_tokens, input_price_per_m = 1.73, output_price_per_m=6.92):
    prompt_cost = (prompt_tokens/1000000) * input_price_per_m
    completion_cost = (completion_tokens/1000000) * output_price_per_m
    
    total_est_cost = prompt_cost + completion_cost
    
    return {
        "prompt_cost": prompt_cost,
        "completion_cost": completion_cost,
        "total_estimated_cost": total_est_cost
    }
    
while True:
    user_input = input("Question: ")
    
    if user_input.lower() in ["exit", "quit"]:
        break

    messages.append({"role": "user", "content": user_input})
    
    start_time = time.time()
    
    try:
        with client.chat.completions.stream(
            model="gpt-4.1",
            messages=messages,
            max_tokens=1000,
            temperature=0.3
        ) as stream:
            print("Streaming response:\n")
            assistant_text = ""
            for event in stream:
                delta = getattr(event, "delta", None)

                if delta is None:
                    continue 

                if isinstance(delta, dict):
                    token = delta.get("content")
                    if token:
                        assistant_text += token
                        print(token, end="", flush=True)

                elif isinstance(delta, str):
                    assistant_text += delta
                    print(delta, end="", flush=True)
                    
            end_time = time.time()
            
            print("\n\n---\nStreaming complete.")
            
            latency = end_time - start_time
            
            print(f"\nLatency: {latency:.2f} seconds")
            
            messages.append({"role": "assistant", "content": assistant_text})
            
            prompt_tokens = len(encoding.encode(str(messages)))
            completion_tokens = len(encoding.encode(assistant_text))
            total_tokens = prompt_tokens + completion_tokens
            
            print(f"Token usage: prompt={prompt_tokens}, completion={completion_tokens}, total={total_tokens}")
            
            if total_tokens > TOKEN_WARNING_LIMIT:
                print("\nWARNING: Token usage is getting high! Consider pruning or summarizing chat history.")
            
    except Exception as e:
        print(f"Error during streaming: {e}")