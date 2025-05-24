
import requests
import sys
import json


DEFAULT_CONFIG = {as
    "model_name": "llama-3b", # EDIT THIS TO "llama-1b" for smaller and faster (but worse) model
    "max_tokens": 100,
    "temperature": 0.0,
    "url": "http://localhost:8000/generate-stream"  # streaming endpoint
}

def send_message(message, config=None):
    if config is None:
        config = DEFAULT_CONFIG
    
    payload = {
        "model_name": config["model_name"],
        "prompt": message,
        "max_tokens": config["max_tokens"],
        "temperature": config["temperature"]
    }
    
    try:
        response = requests.post(
            config["url"],
            json=payload,
            headers={"Content-Type": "application/json"},
            stream=True
        )
        
        if response.status_code == 200:
        
            for chunk in response.iter_content(chunk_size=1, decode_unicode=True):
                if chunk:
                    print(chunk, end='', flush=True)
            print() 
        else:
            print(f"Error: {response.status_code} - {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server. Make sure your server is running on localhost:8000")
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python chat.py \"Your message here\"")
        print("Example: python chat.py \"What is 2+2?\"")
        return
    
    message = " ".join(sys.argv[1:])
    send_message(message)

if __name__ == "__main__":
    main()
