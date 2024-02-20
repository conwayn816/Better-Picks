import requests
import json
import re
import math

def getBets(data):
    bets = []
    for event in data['events']:
        if "NBA" in event['competitionName']:
            if event['homeTeam'] == '' or event['awayTeam'] == '':
                continue
            bet_types = {}
            for types in event['specialFixedOddsMarkets']:
                if types['eventName'] == "Moneyline" or types['eventName'] == "Point Spread" or types['eventName'] == "Total":
                    if types['eventName'] == "Point Spread":
                        types['eventName'] = "Spread"
                    bet_type = types['eventName']
                    bet_type_data = []
                    for outcomes in types['outcomes']:
                        pattern = r'[-+]?\d*\.\d+|\d+'
                        numerical_value = re.findall(pattern, outcomes['name'])
                        if outcomes['price'] < 2.00:
                            odds = str(-math.ceil(((100 / (outcomes['price'] - 1)) / 5.01)) * 5)
                        else:
                            odds = str(+math.ceil((((outcomes['price'] - 1) * 100) / 5.01)) * 5)

                        if types['eventName'] == "Moneyline":
                            team_name = event['homeTeam'] if outcomes['name'].startswith(event['homeTeam']) else event['awayTeam']
                            bet_type_data.append({
                                'event': "NBA",
                                'type': types['eventName'],
                                'team': team_name,
                                'line': "N/A",
                                'odds': odds,
                            })
                        else:
                            team_name = "Over" if "Over" in outcomes['name'] else "Under" if "Under" in outcomes['name'] else event['homeTeam'] if outcomes['name'].startswith(event['homeTeam']) else event['awayTeam']
                            bet_type_data.append({
                                'event': "NBA",
                                'type': types['eventName'],
                                'team': team_name,
                                'line': float(numerical_value[0]),
                                'odds': odds,
                            })
                    bet_types[bet_type] = bet_type_data
            bets.append({
                'home_team': event['homeTeam'],
                'away_team': event['awayTeam'],
                'bets': bet_types
            })
    return bets

if __name__ == "__main__":
    url = "https://api.nj.pointsbet.com/api/v2/sports/basketball/events/featured?includeLive=false"
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

    # Handle exceptions
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data: {e}")

    # Get the bets
    bets = getBets(data)

    # Display of saved bets
    print(json.dumps(bets,indent = 4))