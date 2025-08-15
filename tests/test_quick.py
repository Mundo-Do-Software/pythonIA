import requests

payload = {
    "model": "auto",
    "messages": [{"role": "user", "content": "Olá"}],
    "max_tokens": 50
}

response = requests.post("http://localhost:5000/v1/chat/completions", json=payload, timeout=60)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
