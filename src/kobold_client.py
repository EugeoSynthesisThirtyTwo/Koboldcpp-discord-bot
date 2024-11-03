import requests
from src.config import settings

def generate_response(prompt) -> str:
    data = {
        'prompt': prompt,
        'max_length': 150,  # Control how long the response is
        'temperature': 0.7,  # Adjust for randomness in responses
        'top_k': 50,
        'top_p': 0.9,
        "rep_pen": 1.1,
        "rep_pen_range": 1024,
        "rep_pen_slope": 1,
        "tfs": 1,
        "typical": 1
    }
    
    if settings.koboldcpp_password is None or settings.koboldcpp_password == "":
        headers = None
    else:
        headers = {
            "Authorization": f"Bearer {settings.koboldcpp_password}",
            "Content-Type": "application/json",
            "accept": "application/json"
        }

    try:
        if headers is None:
            response = requests.post(f"{settings.koboldcpp_api_url}/v1/generate", json=data)
        else:
            response = requests.post(f"{settings.koboldcpp_api_url}/v1/generate", json=data, headers=headers)
        
        response_json = response.json()
        if 'text' in response_json:
            return response_json['text']
        else:
            return "Error: No response generated."
    except Exception as e:
        return f"Error communicating with KoboldCpp: {e}"