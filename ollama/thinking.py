from ollama import chat

messages = [
    {
        "role": "user",
        "content": "What is bigger, 9.9 or 9.11?",
    },
]

response = chat("deepseek-r1", messages=messages, think=True)

print(f"Thinking:\n========\n\n{response.message.thinking or ''}")
print(f"\nResponse:\n========\n\n{response.message.content or ''}")
