import requests
import json

BASE_URL = 'http://localhost:5000/api/v1'

# Test user registration
print("Testing user registration...")
register_data = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpassword123"
}
response = requests.post(f'{BASE_URL}/auth/register', json=register_data)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code == 201:
    # Test login
    print("\nTesting user login...")
    login_data = {
        "username": "testuser",
        "password": "testpassword123"
    }
    response = requests.post(f'{BASE_URL}/auth/login', json=login_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        token = data.get('access_token')
        print(f"Login successful! Token: {token[:50]}...")

        # Test protected profile endpoint
        print("\nTesting protected profile endpoint...")
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(f'{BASE_URL}/auth/profile', headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    else:
        print(f"Login failed: {response.text}")
else:
    print(f"Registration failed: {response.text}")