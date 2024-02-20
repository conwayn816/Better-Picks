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
        response.raise_for_status()  
        data = response.json()

        
        with open('fanduel.json', 'w') as f:
            json.dump(data, f, indent=4)

        
        formatted_data = []

        
        for market_id, market_data in data.items():
            if market_data.get('marketName') == 'Moneyline': 
                moneyline_market = market_data  

                
                moneyline_bets = []
                for runner in moneyline_market.get('runners', []):
                    moneyline_bets.append({
                        "event": "NBA",
                        "type": "Moneyline",
                        "team": runner.get('runnerName'),
                        "line": "N/A",  
                        "odds": runner.get('winRunnerOdds', {}).get('americanDisplayOdds', {}).get('americanOddsInt', 'N/A')
                    })

                
                formatted_moneyline_data = {
                    "home_team": moneyline_bets[0]['team'],
                    "away_team": moneyline_bets[1]['team'],
                    "bets": {
                        "Moneyline": moneyline_bets
                    }
                }
                formatted_data.append(formatted_moneyline_data)

    
    print(json.dumps(formatted_data, indent=4))

except requests.exceptions.HTTPError as err:
    if response.status_code == 403:
        print("Error 403: Forbidden - Access to the resource is forbidden.")
    else:
        print(f"HTTP error occurred: {err}")
except Exception as e:
    print(f"An error occurred: {e}")
