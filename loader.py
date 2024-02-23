from database.models import Bets
from database.cleanDB import clean_past_bets
import scripts.betmgm.betmgm as mgmScraper
from mongoengine import connect
import constants
import requests
from datetime import datetime

# Calls on the mgm scraper and inserts into database
def load_mgm_bets() -> None:
    url = constants.mgm_url
    headers = constants.mgm_headers
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
    else:
        raise Exception(str(response.status_code)+ ": " + response.text)

    bet_types = ["Money Line", "Spread", "Totals"]

    # Call scraper and organize data
    extracted_bets = mgmScraper.getBets(data, bet_types)
    organized_bets = mgmScraper.organize_betting_data_ordered(extracted_bets)

    # Save to MongoDB
    connect(db="betterPicks", host=constants.MONGO_URI)
    for game in organized_bets:
        datetime_object = datetime.strptime(game["start_time"], "%Y-%m-%dT%H:%M:%SZ")

        # Check if the game is already in the database
        existing_game = Bets.objects.filter(
            BetProvider="BetMGM",
            GameTime=datetime_object,
            HomeTeam=game["home_team"],
            AwayTeam=game["away_team"],
        ).first()

        # If the game is not in the database, insert it
        if existing_game is None:
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
                        },
                    ],
                },
            )
            bet.save()

    # For testing purposes
    """for game in Bets.objects:
        print(game.HomeTeam, game.AwayTeam)
        print(game.Bets)"""


load_mgm_bets()
