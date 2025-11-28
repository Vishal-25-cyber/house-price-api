import requests
import json
import time

# Wait a moment for the server to start
time.sleep(3)

try:
    # Test the health endpoint
    print("Testing health endpoint...")
    health_response = requests.get("http://localhost:10000/health", timeout=5)
    print(f"Health status: {health_response.status_code}")
    print(f"Health response: {health_response.json()}")
    
    # Test the prediction endpoint
    print("\nTesting prediction endpoint...")
    test_data = {
        "data": [8.3252, 41.0, 6.98, 1.02, 322.0, 2.55, 37.88, -122.23]
    }
    
    pred_response = requests.post("http://localhost:10000/predict", 
                                  json=test_data, 
                                  timeout=5)
    print(f"Prediction status: {pred_response.status_code}")
    print(f"Prediction response: {pred_response.json()}")
    
    print("\n✅ API is working correctly!")
    print("🌐 You can access:")
    print("   - API docs: http://localhost:10000/docs")
    print("   - Gradio UI: http://localhost:10000/gradio")
    print("   - Root page: http://localhost:10000/")

except requests.exceptions.RequestException as e:
    print(f"❌ Error testing API: {e}")
    print("The server might not be running yet or there's a connection issue.")