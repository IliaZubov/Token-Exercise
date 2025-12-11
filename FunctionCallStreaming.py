import os
from openai import AzureOpenAI
import json

api_key = os.getenv("AZURE_API_KEY")
api_version = os.getenv("AZURE_API_VERSION")
azure_endpoint = os.getenv("R_AZURE_ENDPOINT")

client = AzureOpenAI(
    api_key=api_key,
    api_version="2025-03-01-preview",
    azure_endpoint=azure_endpoint
)

def estimate_cost(tokens_input: int, tokens_output: int):
    IN_COST = 1.73
    OUT_COST = 6.92
    cost_in = tokens_input / 1_000_000 * IN_COST
    cost_out = tokens_output / 1_000_000 * OUT_COST
    return {"prompt_cost": cost_in, "completion_cost": cost_out, "total": cost_in + cost_out}

tools = [
    {
        "type": "function",
        "name": "estimate_cost",
        "function": {
            "name": "estimate_cost",
            "description": "Estimate cost based on ACTUAL tokens used.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]

messages = [
    {"type": "message", "role": "system", "content": (
            "You are a bike mechanic expert. If user asks for cost, call estimate_cost with no arguments."
        )}
]
    
while True:
    user_input = input("Question: ")

    if user_input.lower() in ["exit", "quit"]:
        break

    messages.append({"type": "message", "role": "user", "content": user_input})
    
    tool_call = None
    input_tokens_used = None
    output_tokens_used = None
    try:
        response = client.responses.create(
            model="gpt-4.1",
            input=messages,
            tools=tools,
            tool_choice="auto",
            stream=True
        )
        
        print("\nAssistant: ", end="")
        
        for event in response:
                
            if event.type == "response.output_text.delta":
                print(event.delta, end="")

            if event.type == "response.output_item.added":
                if hasattr(event, "item") and event.item.type == "function_call":
                    tool_call = event.item

            if event.type == "response.completed":
                usage = event.response.usage
                input_tokens_used = usage.input_tokens
                output_tokens_used = usage.output_tokens
    except Exception as e:
        print("Request failed with error:", e)
            
    print("\n\n---\n")
    
    if not tool_call:
        continue

    result = estimate_cost(input_tokens_used, output_tokens_used)
    
    messages.append({
    "type": "function_call",
    "call_id": tool_call.call_id,
    "name": tool_call.name,
    "arguments": tool_call.arguments
    })
    
    messages.append({
    "type": "function_call_output",
    "call_id": tool_call.call_id,
    "output": json.dumps(result)
    })

    print(f"\nEstimated costs based on token usage: {result["total"]:.5f} €")