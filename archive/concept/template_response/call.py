import os
import json
import requests

YOUR_API_KEY = os.environ.get('OPENAI_API_KEY')
if not YOUR_API_KEY:
    raise RuntimeError("OPENAI_API_KEY environment variable not set")

with open('initiative_template.json') as f:
    tmpl = json.load(f)

# Get the tools from the template
tools = tmpl['example_scenario']['initial_tool_definition']['session.update']['tools']

# Register the tools with the chat completions API
response = requests.post(
    "https://api.openai.com/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {YOUR_API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": "gpt-4-1106-preview",  # or another model that supports function calling
        "messages": [{"role": "system", "content": "You are a helpful assistant."}],
        "tools": tools
    }
)

if response.status_code == 200:
    print("Tools registered successfully")
    print("Response:", response.json())
else:
    print(f"Error registering tools: {response.status_code}")
    print("Response:", response.text)