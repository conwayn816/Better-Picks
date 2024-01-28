# Nate
import requests
import constants

def getBets(data, bet_types):
    bets = []
    

    return bets


if __name__ == "__main__":
    url = constants.url
    headers = constants.headers
    response = requests.get(url, headers=headers)   

    if response.status_code == 200:
        data = response.json()
    else:
        print("Error: " + str(response.status_code))

    
    bet_types = ['Moneyline', 'Spread'] 

    bets = getBets(data, bet_types)

    for bet in bets:
        print(bet)

