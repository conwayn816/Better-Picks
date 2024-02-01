# Nate
import requests
import constants

def getBets(data, bet_types):
    bets = []
    items = data.get("widgets")[0].get("payload").get("items")
    fixtures = items[0].get("activeChildren")[0].get("payload").get("fixtures")
    
    games = [] #stores each game in a list
    for fixture in fixtures:
        games.append(fixture.get("games"))
    
    
    
    

    return bets


if __name__ == "__main__":
    url = constants.url
    headers = constants.headers
    response = requests.get(url, headers=headers)   

    if response.status_code == 200:
        data = response.json()
    else:
        print("Error: " + str(response.status_code))

    
    bet_types = ['Moneyline', 'Spread', 'Total Points'] 

    getBets(data, bet_types)


