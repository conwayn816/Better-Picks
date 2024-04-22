from flask import Flask, render_template, redirect, url_for, request, jsonify
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
    return render_template('total.html', box_items=game_bets.values(), active_view=active_view, current_date=start_of_day)

@app.route('/search', methods=['POST'])
def search():
    search_input = request.json.get('searchInput', '')

    # Get the JSON data displayed for the current day
    start_of_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)
    game_bets = db.bets.find({'GameTime': {'$gte': start_of_day, '$lt': end_of_day}})

    # Perform the search based on the input query
    filtered_game_data = []
    for doc in game_bets:
        if search_input.lower() in doc['HomeTeam'].lower() or search_input.lower() in doc['AwayTeam'].lower():
            filtered_game_data.append(doc)

    # Convert the filtered game data to a list of dictionaries
    filtered_game_data_dicts = [game_data for game_data in filtered_game_data]

    return jsonify(filtered_game_data_dicts)

if __name__ == '__main__':
    load_bets()
    app.run(debug=True)
