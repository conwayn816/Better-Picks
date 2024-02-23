from mongoengine import *
import betmgm as scraper
import constants
import requests
import json
from datetime import datetime


class Bets(Document):
    BetProvider = StringField(required=True)
    GameTime = DateTimeField(required=True)
    HomeTeam = StringField(required=True)
    AwayTeam = StringField(required=True)
    Bets = DictField(
        Spread=ListField(
            DictField(
                Team=StringField(required=True),
                Line=FloatField(required=True),
                Odds=FloatField(required=True),
            )
        ),
        Total=ListField(
            DictField(
                Team=StringField(required=True),
                Line=FloatField(required=True),
                Odds=FloatField(required=True),
            )
        ),
        Moneyline=ListField(
            DictField(
                Team=StringField(required=True),
                Odds=FloatField(required=True),
            )
        ),
    )


if __name__ == "__main__":
    url = constants.url
    headers = constants.headers
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
    else:
        print("Error: " + str(response.status_code))

    bet_types = ["Money Line", "Spread", "Totals"]

    extracted_bets = scraper.getBets(data, bet_types)
    organized_bets = scraper.organize_betting_data_ordered(extracted_bets)

    # Save to MongoDB
    connect(db='betterPicks', host=constants.MONGO_URI)
    for game in organized_bets:
        datetime_object = datetime.strptime(game["start_time"], "%Y-%m-%dT%H:%M:%SZ")
        bet = Bets(
            BetProvider="BetMGM",
            GameTime=datetime_object,
            HomeTeam=game["home_team"],
            AwayTeam=game["away_team"],
            Bets={
                "Spread": [
                    {
                        "Team": game["bets"]["Spread"][0]["team"],
                        "Line": game["bets"]["Spread"][0]["line"],
                        "Odds": game["bets"]["Spread"][0]["odds"],
                    },
                    {
                        "Team": game["bets"]["Spread"][1]["team"],
                        "Line": game["bets"]["Spread"][1]["line"],
                        "Odds": game["bets"]["Spread"][1]["odds"],
                    },
                ],
                "Total": [
                    {
                        "Team": game["bets"]["Total"][0]["team"],
                        "Line": game["bets"]["Total"][0]["line"],
                        "Odds": game["bets"]["Total"][0]["odds"],
                    },
                    {
                        "Team": game["bets"]["Total"][1]["team"],
                        "Line": game["bets"]["Total"][1]["line"],
                        "Odds": game["bets"]["Total"][1]["odds"],
                    },
                ],
                "Moneyline": [
                    {
                        "Team": game["bets"]["Moneyline"][0]["team"],
                        "Odds": game["bets"]["Moneyline"][0]["odds"],
                    },
                    {
                        "Team": game["bets"]["Moneyline"][1]["team"],
                        "Odds": game["bets"]["Moneyline"][1]["odds"],
                    }
                ],
            },
        )
        bet.save()

    # Print to console
    for game in Bets.objects:
        print(game.HomeTeam, game.AwayTeam)
        print(game.Bets)

    prettifiedJson = json.dumps(organized_bets, indent=4)
    # print(prettifiedJson)
