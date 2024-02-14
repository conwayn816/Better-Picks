# Nate
import requests
import constants
import json

def getBets(data, bet_types):
    bets = []
    items = data.get("widgets")[0].get("payload").get("items")
    fixtures = items[0].get("activeChildren")[0].get("payload").get("fixtures")

    events = []  # stores each fixture in a list
    for fixture in fixtures:
        events.append(fixture)

    matchups = {}  # stores the event id and the matchup
    for event in events:
        id = event.get("id")
        matchup = event.get("name").get("value")
        matchups[id] = matchup

    for event in events:
        for offer in event.get("optionMarkets"):
            if offer.get("name").get("value") in bet_types:
                for result in offer.get("options"):
                    current_team = result.get("name").get("value")
                    line = None
                    if "Over" in current_team or "Under" in current_team:
                        line = current_team
                        team = "N/A"
                    elif "Spread" in offer.get("name").get("value"):
                        l = current_team.split(" ")
                        team = ""
                        for i in range(0,(len(l)-1)):
                            team += l[i] + " "
                        line = l[len(l)-1]
                    else:
                        team = current_team
                    bets.append(
                        {
                            "event": matchups.get(event.get("id")),
                            "type": offer.get("name").get("value"),
                            "team": team,
                            "line": line,
                            "odds": result.get("price").get("americanOdds"),
                        }
                    )

    return bets


def organize_betting_data_ordered(bets):
    organized_games = []
    current_game = None

    for bet in bets:
        if current_game is None or (len(current_game["bets"]["Spread"]) == 2 and
                                    len(current_game["bets"]["Total"]) == 2 and
                                    len(current_game["bets"]["Moneyline"]) == 2):
            current_game = {
                "home_team": "",  # Placeholder for home team
                "away_team": bet["team"],  # first bet is away team
                "bets": {
                    "Spread": [],  # Add the first spread bet
                    "Total": [],  # Placeholder for total bets
                    "Moneyline": [],  # Placeholder for moneyline bets
                },
            }
            organized_games.append(current_game)
        if bet["type"] == "Spread":
            if current_game is None or len(current_game["bets"]["Spread"]) == 0:
                current_game["bets"]["Spread"].append(bet)
            else:
                # Second spread bet is the home team for the current game
                current_game["home_team"] = bet["team"]
                current_game["bets"]["Spread"].append(bet)
        elif bet["type"] == "Totals" and current_game is not None:
            # Add total bet to the current game
            current_game["bets"]["Total"].append(bet)
        elif bet["type"] == "Money Line" and current_game is not None:
            # Add moneyline bet to the current game
            current_game["bets"]["Moneyline"].append(bet)

    return organized_games


if __name__ == "__main__":
    url = constants.url
    headers = constants.headers
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
    else:
        print("Error: " + str(response.status_code))

    bet_types = ["Money Line", "Spread", "Totals"]

    extracted_bets = getBets(data, bet_types)
    organized_bets = organize_betting_data_ordered(extracted_bets)
    prettifiedJson = json.dumps(organized_bets, indent=4)
    print(prettifiedJson)
    