import requests
import json

def caesar_fetch(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # TEMP PRINT DATA
        print(json.dumps(data, indent=4))

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data: {e}")

if __name__ == "__main__":
    api_url = "https://api.americanwagering.com/regions/us/locations/pa/brands/czr/sb/v3/cannedparlays/basketball"
    caesar_fetch(api_url)