import ollama

response = ollama.chat(model="gemma3:1b", messages=[{"role": "user", "content": "What is Transformers. Explain with simple example"}])

print(response['message']['content'])
