import requests
import json

# Test GET request
print("Testing GET /api/v1/prompts")
response = requests.get('http://localhost:5000/api/v1/prompts')
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Number of prompts: {len(data)}")
else:
    print(f"Error: {response.text}")

# Test POST request
print("\nTesting POST /api/v1/prompts")
payload = {
    "project_name": "API Test",
    "project_description": "Testing API creation",
    "project_objectives": "Verify API functionality",
    "category": "texto",
    "language": "python",
    "temperature": "0.7",
    "tone": "formal"
}
response = requests.post('http://localhost:5000/api/v1/prompts',
                        json=payload,
                        headers={'Content-Type': 'application/json'})
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")