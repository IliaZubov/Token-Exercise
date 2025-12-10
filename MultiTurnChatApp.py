import os
from openai import AzureOpenAI
import json

api_key = os.getenv("AZURE_API_KEY")
api_version = os.getenv("AZURE_API_VERSION")
azure_endpoint = os.getenv("AZURE_ENDPOINT")

client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=azure_endpoint
)

def estimate_cost(tokens_input: int, tokens_output: int):
    INPUT_PRICE_PER_M = 1.73
    OUTPUT_PRICE_PER_M = 6.92

    prompt_cost = (tokens_input / 1_000_000) * INPUT_PRICE_PER_M
    completion_cost = (tokens_output / 1_000_000) * OUTPUT_PRICE_PER_M
    total = prompt_cost + completion_cost

    return {
        "prompt_cost": prompt_cost,
        "completion_cost": completion_cost,
        "total_estimated_cost": total,
    }
    
tools = [
    {
        "type": "function",
        "function": {
            "name": "estimate_cost",
            "description": "Estimate cost based on token usage.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tokens_input": {"type": "integer"},
                    "tokens_output": {"type": "integer"}
                },
                "required": ["tokens_input", "tokens_output"]
            }
        }
    }
]

messages = [
    {"role": "system", "content": "You are a bike mechanic expert."}
]

while True:
    user_input = input("Question: ")
    
    if user_input.lower() in ["exit", "quit"]:
        break

    messages.append({"role": "user", "content": user_input})

    assistant_reply = ""
    
    handled_tool_call = False
    
    while True:

        response = client.chat.completions.create(
            model="gpt-4.1", 
            messages=messages,
            tools=tools,
            temperature=0.1,
            max_tokens=500
        )
        
        tool_calls = response.choices[0].message.tool_calls
        
        

        if tool_calls:
            call = tool_calls[0]
            fn_name = call.function.name
            args = json.loads(call.function.arguments)

            if fn_name == "estimate_cost":

                messages.append({
                    "role": "assistant",
                    "tool_calls": response.choices[0].message.tool_calls
                })

                result = estimate_cost(**args)
                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": json.dumps(result)
                })

                final_response = client.chat.completions.create(
                    model="gpt-4.1",
                    messages=messages
                )

                assistant_reply = final_response.choices[0].message.content
                messages.append({"role": "assistant", "content": assistant_reply})

                print("\nAnswer:", assistant_reply, "\n")
                handled_tool_call = True
                break
        
        chunk = response.choices[0].message.content
        
        assistant_reply += chunk
        
        if response.choices[0].finish_reason != "length":
            break
        
        messages.append({"role": "assistant", "content": chunk})
                
        messages.append({"role": "user", "content": "Please provide a shorter/summary response."})
    
    if handled_tool_call:
        continue   
    messages.append({"role": "assistant", "content": assistant_reply})
    
    print("\nAnswer:", assistant_reply, "\n")    
        
