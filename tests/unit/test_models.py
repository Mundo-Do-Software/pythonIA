import requests

# Testar lista de modelos
response = requests.get("http://localhost:5000/v1/models")
print("📋 Modelos disponíveis:")
print(response.json())
