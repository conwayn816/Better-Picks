# Nate
import requests
import constants


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
        for offer in event.get("games"):
            if offer.get("name").get("value") in bet_types:
                for result in offer.get("results"):
                    current_team = result.get("name").get("value")
                    line = None
                    if "Over" in current_team or "Under" in current_team:
                        line = current_team
                        current_team = "N/A"
                    else:
                        current_team = current_team
                    bets.append(
                        {
                            "event": matchups.get(event.get("id")),
                            "type": offer.get("name").get("value"),
                            "team": current_team,
                            "line": line,
                            "odds": result.get("americanOdds"),
                        }
                    )

    return bets


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

    for bet in extracted_bets:
        print(bet)
        print("\n")
