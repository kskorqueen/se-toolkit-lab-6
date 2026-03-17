#!/usr/bin/env python3
from openai import OpenAI

LLM_API_KEY = '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'
LLM_API_BASE = 'https://openrouter.ai/api/v1'
LLM_MODEL = 'meta-llama/llama-3.3-70b-instruct:free'

client = OpenAI(api_key=LLM_API_KEY, base_url=LLM_API_BASE)

messages = [
    {'role': 'system', 'content': 'Use tools to answer. Do not output commentary.'},
    {'role': 'user', 'content': 'List files in backend folder'}
]

tools = [{
    'type': 'function',
    'function': {
        'name': 'list_files',
        'description': 'List files',
        'parameters': {
            'type': 'object',
            'properties': {
                'path': {'type': 'string'}
            },
            'required': ['path']
        }
    }
}]

response = client.chat.completions.create(
    model=LLM_MODEL,
    messages=messages,
    tools=tools,
    tool_choice='auto'
)

print('First response:')
print('Content:', response.choices[0].message.content)
print('Tool calls:', response.choices[0].message.tool_calls)

# Simulate tool result
if response.choices[0].message.tool_calls:
    messages.append(response.choices[0].message)
    messages.append({
        'role': 'tool',
        'tool_call_id': response.choices[0].message.tool_calls[0].id,
        'content': 'app\ntests'
    })
    
    response2 = client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
        tools=tools,
        tool_choice='auto'
    )
    
    print('\nSecond response:')
    print('Content:', response2.choices[0].message.content)
    print('Tool calls:', response2.choices[0].message.tool_calls)
