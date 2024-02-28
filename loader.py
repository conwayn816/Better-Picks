# Database imports
from database.models import Bets
from database.cleanDB import clean_past_bets

# Import scrapers
import scripts.betmgm.betmgm as mgmScraper
import scripts.draftkings.draftkings as draftkingsScraper
import scripts.caesars as caesarsScraper
import scripts.pointsbet as pointsbetScraper

# Import mongoengine for db interaction
from mongoengine import connect

# Import constants
import constants

# Import other libraries
import requests
from datetime import datetime


def load_dk_bets() -> None:
    response = requests.get(constants.dk_url)
    if response.status_code == 200:
        data = response.json()
    else:
        raise Exception(str(response.status_code) + ": " + response.text)
    bet_types = ["Moneyline", "Spread"]
    extracted_bets = draftkingsScraper.extract_bets(data, bet_types)
    event_start_dates = {}
    for subcategory in data["featuredDisplayGroup"]["featuredSubcategories"]:
        for event in subcategory.get("events", []):
            event_start_dates[event["eventId"]] = event["startDate"]
    res = draftkingsScraper.organize_betting_data_ordered(
        extracted_bets, event_start_dates
    )
    for game in res:
        for bet_type, bets in game["bets"].items():
            for bet in bets:
                bet.pop("eventId", None)
    connect(
        db="betterPicks",
        host=constants.MONGO_URI,
    )
    for game in res:
        game_time_obj = datetime.strptime(game["GameTime"], "%Y-%m-%dT%H:%M:%SZ")
        existing_game = Bets.objects.filter(
            BetProvider="DraftKings",
            GameTime=game_time_obj,
            HomeTeam=game["home_team"],
            AwayTeam=game["away_team"],
        ).first()
        if existing_game is None:
            bet = Bets(
                BetProvider="DraftKings",
                GameTime=game_time_obj,
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


# Calls on the mgm scraper and inserts into database
def load_mgm_bets() -> None:
    url = constants.mgm_url
    headers = constants.mgm_headers
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
    else:
        raise Exception(str(response.status_code) + ": " + response.text)

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

    """ TESTING
    for game in Bets.objects:
        print(game.HomeTeam, game.AwayTeam)
        print(game.Bets)
    """


def load_pb_bets() -> None:
    url = constants.pb_url
    headers = constants.pb_headers
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
    else:
        raise Exception(str(response.status_code) + ": " + response.text)

    bets = pointsbetScraper.getBets(data)

    connect(db="betterPicks", host=constants.MONGO_URI)
    for game in bets:
        datetime_object = datetime.strptime(game["start_time"], "%Y-%m-%d %H:%M:%S")
        existing_game = Bets.objects.filter(
            BetProvider="PointsBet",
            GameTime=datetime_object,
            HomeTeam=game["home_team"],
            AwayTeam=game["away_team"],
        ).first()
        if existing_game is None:
            bet = Bets(
                BetProvider="PointsBet",
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
            print(bet.HomeTeam, bet.AwayTeam, bet.GameTime, bet.Bets)
            #bet.save()
    ''' TESTING
    for game in Bets.objects:
        print(game.HomeTeam, game.AwayTeam)
        print(game.Bets)'''


""" ACTUAL CALLS
load_mgm_bets()
load_dk_bets()
"""
load_pb_bets()
