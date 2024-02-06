import requests
import json

# Function to fetch data from PointsBet API and save it to a file
def pb_fetch_and_save(url, filename):
    # Set the user-agent to avoid 403 Forbidden error
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    # Fetch data from the API and save it to a file
    try:
        # Fetch data from the API
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # TEMP PRINT DATA
        print(json.dumps(data, indent=4))

    # Handle exceptions
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data: {e}")

if __name__ == "__main__":
    api_url = "https://api.nj.pointsbet.com/api/v2/competitions/105/events/featured?includeLive=false&page=1"
    output_file = "pointsbet_api_data.json"
    pb_fetch_and_save(api_url, output_file)