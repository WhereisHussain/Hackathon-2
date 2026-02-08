import requests
import json

BASE_URL = "http://localhost:8000"
USER_ID = "ziakhan"

def test_chat():
    payload = {
        "message": "Add a task to buy bread"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/{USER_ID}/chat", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Testing Chat Endpoint...")
    test_chat()
