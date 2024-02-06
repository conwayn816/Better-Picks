import requests
import json

url = 'https://sbapi.nj.sportsbook.fanduel.com/api/content-managed-page?page=CUSTOM&customPageId=nba&pbHorizontal=false&_ak=FhMFpcPWXMeyZxOx&timezone=America%2FNew_York'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Timezone': 'America/New_York',
    
}

try:
    with requests.Session() as session:
        response = session.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        data = response.json()
        
        print(json.dumps(data, indent=4))
        
        with open('fanduel.json', 'w') as f:
            json.dump(data, f, indent=4)
    
except requests.exceptions.HTTPError as err:
    if response.status_code == 403:
        print("Error 403: Forbidden - Access to the resource is forbidden.")
    else:
        print(f"HTTP error occurred: {err}")
except Exception as e:
    print(f"An error occurred: {e}")
