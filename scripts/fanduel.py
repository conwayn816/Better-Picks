#Andres
#https://sbapi.nj.sportsbook.fanduel.com/api/content-managed-page?page=CUSTOM&customPageId=nba&pbHorizontal=false&_ak=FhMFpcPWXMeyZxOx&timezone=America%2FNew_York

import requests

url = "https://sbapi.nj.sportsbook.fanduel.com/api/content-managed-page?page=CUSTOM&customPageId=nba&pbHorizontal=false&_ak=FhMFpcPWXMeyZxOx&timezone=America%2FNew_York"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    moneylines = []

    for market_id, market_data in data.items():
        if 'marketType' in market_data and market_data['marketType'] == 'MONEY_LINE':
            runners = market_data.get('runners', [])
            for runner in runners:
                moneyline_info = {
                    'runnerName': runner['runnerName'],
                    'winRunnerOdds': runner['winRunnerOdds']['americanDisplayOdds']['americanOdds']
                }
                moneylines.append(moneyline_info)

    print("Moneylines:", moneylines)

else:
    print(f"Error: Unable to fetch data. Status Code: {response.status_code}")

