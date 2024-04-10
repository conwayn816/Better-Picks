from flask import Flask, render_template, redirect, url_for
from database.models import Bets
from pymongo import MongoClient
import constants
from teamMap import TEAM_MAP
from loader import load_bets
from datetime import datetime, timedelta
import pytz

# Create timezone objects for UTC and EST
utc = pytz.timezone("UTC")
est = pytz.timezone("US/Eastern")

# TEMP DATABASE FOR TESTING
'''
Bets = [
    {
        "BetProvider": "DraftKings",
        "GameTime": "2024-04-01 12:00:00",
        "HomeTeam": "Home Team",
        "AwayTeam": "Away Team",
        "Bets": {
            "Spread": [
                {"Team": "Home Team", "Line": -3.5, "Odds": 100},
                {"Team": "Away Team", "Line": 3.5, "Odds": -100},
            ],
            "Total": [
                {"Team": "Over", "Line": 210.5, "Odds": 100},
                {"Team": "Under", "Line": 210.5, "Odds": -100},
            ],
            "Moneyline": [
                {"Team": "Home Team", "Odds": -110},
                {"Team": "Away Team", "Odds": 100},
            ],
        },
    },
    {
        "BetProvider": "Caesers Sportsbook",
        "GameTime": "2024-04-01 12:00:00",
        "HomeTeam": "Home Team",
        "AwayTeam": "Away Team",
        "Bets": {
            "Spread": [
                {"Team": "Home Team", "Line": -4.5, "Odds": 100},
                {"Team": "Away Team", "Line": 4.5, "Odds": -100},
            ],
            "Total": [
                {"Team": "Over", "Line": 224.5, "Odds": 200},
                {"Team": "Under", "Line": 224.5, "Odds": -200},
            ],
            "Moneyline": [
                {"Team": "Home Team", "Odds": -100},
                {"Team": "Away Team", "Odds": -100},
            ],
        },
    },
    {
        "BetProvider": "PointsBet",
        "GameTime": "2024-04-01 12:00:00",
        "HomeTeam": "Home Team",
        "AwayTeam": "Away Team",
        "Bets": {
            "Spread": [
                {"Team": "Home Team", "Line": -3.5, "Odds": 100},
                {"Team": "Away Team", "Line": 3.5, "Odds": -100},
            ],
            "Total": [
                {"Team": "Over", "Line": 212.5, "Odds": 100},
                {"Team": "Under", "Line": 212.5, "Odds": -100},
            ],
            "Moneyline": [
                {"Team": "Home Team", "Odds": -110},
                {"Team": "Away Team", "Odds": 100},
            ],
        },
    },
    {
        "BetProvider": "BetMGM",
        "GameTime": "2024-04-01 12:00:00",
        "HomeTeam": "Home Team",
        "AwayTeam": "Away Team",
        "Bets": {
            "Spread": [
                {"Team": "Home Team", "Line": -4.5, "Odds": 100},
                {"Team": "Away Team", "Line": 4.5, "Odds": -100},
            ],
            "Total": [
                {"Team": "Over", "Line": 200.5, "Odds": 200},
                {"Team": "Under", "Line": 200.5, "Odds": -200},
            ],
            "Moneyline": [
                {"Team": "Home Team", "Odds": -100},
                {"Team": "Away Team", "Odds": -100},
            ],
        },
    },
]
'''

client = MongoClient(constants.MONGO_URI)
db = client.betterPicks


app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('moneyline'))

@app.route('/refresh', methods=['POST'])
def refresh():
    load_bets()
    return '', 200


@app.route('/moneyline', methods=['GET', 'POST'])
def moneyline():
    active_view = 'Moneyline'
    current_date = datetime.now().strftime('%Y-%m-%d')
    start_of_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)
    game_bets = {}
    for doc in db.bets.find({'GameTime': {'$gte': start_of_day, '$lt': end_of_day}}):
        if doc['HomeTeam'] in TEAM_MAP:
            hometeam = TEAM_MAP[doc['HomeTeam']]
        else:
            hometeam = doc['HomeTeam']
        if doc['AwayTeam'] in TEAM_MAP:
            awayteam = TEAM_MAP[doc['AwayTeam']]
        else:
            awayteam = doc['AwayTeam']
        game_key = (hometeam, awayteam)
        if game_key not in game_bets:
            game_bets[game_key] = {'HomeTeam': hometeam, 'AwayTeam': awayteam, 'bets': []}
        # Convert the game_time from UTC to EST
        game_time = doc["GameTime"].replace(tzinfo=utc).astimezone(est).strftime("%I:%M %p EST")
        game_bets[game_key]['GameTime'] = game_time
        game_bets[game_key]['bets'].append({
            'BetProvider': doc['BetProvider'],
            'HomeTeamBet': doc['Bets']['Moneyline'][0],
            'AwayTeamBet': doc['Bets']['Moneyline'][1]
        })
    
    return render_template('moneyline.html', box_items=game_bets.values(), active_view=active_view, current_date=start_of_day)

@app.route('/spread', methods=['GET', 'POST'])
def spread():
    active_view = 'Spread'
    current_date = datetime.now().strftime('%Y-%m-%d')
    start_of_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)
    game_bets = {}
    for doc in db.bets.find({'GameTime': {'$gte': start_of_day, '$lt': end_of_day}}):
        if doc['HomeTeam'] in TEAM_MAP:
            hometeam = TEAM_MAP[doc['HomeTeam']]
        else:
            hometeam = doc['HomeTeam']
        if doc['AwayTeam'] in TEAM_MAP:
            awayteam = TEAM_MAP[doc['AwayTeam']]
        else:
            awayteam = doc['AwayTeam']
        game_key = (hometeam, awayteam)
        if game_key not in game_bets:
            game_bets[game_key] = {'HomeTeam': hometeam, 'AwayTeam': awayteam, 'bets': []}
        bet = {'BetProvider': doc['BetProvider']}

        current_team = doc['Bets']['Spread'][0]['Team']
        if current_team not in TEAM_MAP:
            if current_team == hometeam:
                bet['HomeTeamBet'] = doc['Bets']['Spread'][0]
                bet['AwayTeamBet'] = doc['Bets']['Spread'][1]
            else:
                bet['HomeTeamBet'] = doc['Bets']['Spread'][1]
                bet['AwayTeamBet'] = doc['Bets']['Spread'][0]
        else: 
            if TEAM_MAP[current_team] == hometeam:
                bet['HomeTeamBet'] = doc['Bets']['Spread'][0]
                bet['AwayTeamBet'] = doc['Bets']['Spread'][1]
            else:
                bet['HomeTeamBet'] = doc['Bets']['Spread'][1]
                bet['AwayTeamBet'] = doc['Bets']['Spread'][0]

        game_bets[game_key]['bets'].append(bet)
    '''
    for bet in Bets:
        game_key = (bet['HomeTeam'], bet['AwayTeam'])
        if game_key not in game_bets:
            game_bets[game_key] = {'HomeTeam': bet['HomeTeam'], 'AwayTeam': bet['AwayTeam'], 'bets': []}
        game_bets[game_key]['bets'].append({
            'BetProvider': bet['BetProvider'],
            'HomeTeamBet': bet['Bets']['Spread'][0],
            'AwayTeamBet': bet['Bets']['Spread'][1]
        })
    '''
    return render_template('spread.html', box_items=game_bets.values(), active_view=active_view, current_date=start_of_day)

@app.route('/total', methods=['GET', 'POST'])
def total():
    active_view = 'Total'
    current_date = datetime.now().strftime('%Y-%m-%d')
    start_of_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)
    game_bets = {}
    for doc in db.bets.find({'GameTime': {'$gte': start_of_day, '$lt': end_of_day}}):
        if doc['HomeTeam'] in TEAM_MAP:
            hometeam = TEAM_MAP[doc['HomeTeam']]
        else:
            hometeam = doc['HomeTeam']
        if doc['AwayTeam'] in TEAM_MAP:
            awayteam = TEAM_MAP[doc['AwayTeam']]
        else:
            awayteam = doc['AwayTeam']
        game_key = (hometeam, awayteam)
        if game_key not in game_bets:
            game_bets[game_key] = {'HomeTeam': hometeam, 'AwayTeam': awayteam, 'bets': []}
        game_bets[game_key]['bets'].append({
            'BetProvider': doc['BetProvider'],
            'HomeTeamBet': doc['Bets']['Total'][0],
            'AwayTeamBet': doc['Bets']['Total'][1]
        })
    '''
    for bet in Bets:
        game_key = (bet['HomeTeam'], bet['AwayTeam'])
        if game_key not in game_bets:
            game_bets[game_key] = {'HomeTeam': bet['HomeTeam'], 'AwayTeam': bet['AwayTeam'], 'bets': []}
        game_bets[game_key]['bets'].append({
            'BetProvider': bet['BetProvider'],
            'HomeTeamBet': bet['Bets']['Total'][0],
            'AwayTeamBet': bet['Bets']['Total'][1]
        })
    '''
    return render_template('total.html', box_items=game_bets.values(), active_view=active_view, current_date=start_of_day)
'''
need to add uname settings function, pword settings function, friends function, and account history
function once we have another mongo db collection setup that includes users/pwords, friends 
associated w/ users, and account wins/losses
'''
if __name__ == '__main__':
    load_bets()
    app.run(debug=True)
