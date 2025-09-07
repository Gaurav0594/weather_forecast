
import os
from dotenv import load_dotenv
import requests

def test_environment():
    """Test if environment is properly set up"""
    print("Testing environment setup...")
    
    # Test dotenv
    load_dotenv()
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if api_key:
        print(f"✓ Environment variables loaded successfully")
        print(f"✓ API Key found: {api_key[:8]}...")
    else:
        print("✗ API Key not found in environment variables")
        return False
    
    # Test requests
    try:
        response = requests.get("https://httpbin.org/get", timeout=5)
        if response.status_code == 200:
            print("✓ Requests library working correctly")
        else:
            print("✗ Requests library test failed")
            return False
    except Exception as e:
        print(f"✗ Requests library error: {e}")
        return False
    
    print("✓ Environment setup complete and working!")
    return True

if __name__ == "__main__":
    test_environment()
