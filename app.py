from flask import Flask, render_template, redirect, url_for, request, jsonify
from database.models import Bets
import mongoengine
import constants
from teamMap import TEAM_MAP
from loader import load_bets
from datetime import datetime, timedelta
import pytz

# Create timezone objects for UTC and EST
utc = pytz.timezone("UTC")
est = pytz.timezone("US/Eastern")
db = mongoengine.connect(db="betterPicks", host=constants.MONGO_URI)


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
    for bet in Bets.objects(GameTime__gte=start_of_day, GameTime__lt=end_of_day):
        if bet["HomeTeam"] in TEAM_MAP:
            hometeam = TEAM_MAP[bet["HomeTeam"]]
        else:
            hometeam = bet["HomeTeam"]
        if bet["AwayTeam"] in TEAM_MAP:
            awayteam = TEAM_MAP[bet["AwayTeam"]]
        else:
            awayteam = bet["AwayTeam"]
        game_key = (hometeam, awayteam)
        if game_key not in game_bets:
            game_bets[game_key] = {
                "HomeTeam": hometeam,
                "AwayTeam": awayteam,
                "bets": [],
            }
        # Convert the game_time from UTC to EST
        game_time = (
            bet["GameTime"].replace(tzinfo=utc).astimezone(est).strftime("%I:%M %p EST")
        )
        game_bets[game_key]["GameTime"] = game_time
        if bet["BetProvider"] == "BetMGM" or bet["BetProvider"] == "DraftKings":
            game_bets[game_key]["bets"].append(
                {
                    "BetProvider": bet["BetProvider"],
                    "HomeTeamBet": bet["Bets"]["Moneyline"][1],
                    "AwayTeamBet": bet["Bets"]["Moneyline"][0],
                    "BetType": "Moneyline",
                }
            )
        else:
            game_bets[game_key]["bets"].append(
                {
                    "BetProvider": bet["BetProvider"],
                    "HomeTeamBet": bet["Bets"]["Moneyline"][0],
                    "AwayTeamBet": bet["Bets"]["Moneyline"][1],
                    "BetType": "Moneyline",
                }
            )

    return render_template('moneyline.html', box_items=game_bets.values(), active_view=active_view, current_date=start_of_day)

@app.route('/spread', methods=['GET', 'POST'])
def spread():
    active_view = 'Spread'
    current_date = datetime.now().strftime('%Y-%m-%d')
    start_of_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)
    game_bets = {}
    for bet in Bets.objects(GameTime__gte=start_of_day, GameTime__lt=end_of_day):   
        if bet["HomeTeam"] in TEAM_MAP:
            hometeam = TEAM_MAP[bet["HomeTeam"]]
        else:
            hometeam = bet["HomeTeam"]
        if bet["AwayTeam"] in TEAM_MAP:
            awayteam = TEAM_MAP[bet["AwayTeam"]]
        else:
            awayteam = bet["AwayTeam"]
        game_key = (hometeam, awayteam)
        if game_key not in game_bets:
            game_bets[game_key] = {
                "HomeTeam": hometeam,
                "AwayTeam": awayteam,
                "bets": [],
            }
        bet_data = {"BetProvider": bet["BetProvider"]}
        if "Bets" in bet and "Spread" in bet["Bets"] and len(bet["Bets"]["Spread"]) > 0:
            current_team = bet["Bets"]["Spread"][0]["Team"]
            # Convert the game_time from UTC to EST
            game_time = (bet["GameTime"].replace(tzinfo=utc).astimezone(est).strftime("%I:%M %p EST"
            ))
            game_bets[game_key]["GameTime"] = game_time
            if current_team not in TEAM_MAP:
                if current_team == hometeam:
                    bet_data["HomeTeamBet"] = bet["Bets"]["Spread"][0]
                    bet_data["AwayTeamBet"] = bet["Bets"]["Spread"][1]
                else:
                    bet_data["HomeTeamBet"] = bet["Bets"]["Spread"][1]
                    bet_data["AwayTeamBet"] = bet["Bets"]["Spread"][0]
            else:
                if TEAM_MAP[current_team] == hometeam:
                    bet_data["HomeTeamBet"] = bet["Bets"]["Spread"][0]
                    bet_data["AwayTeamBet"] = bet["Bets"]["Spread"][1]
                else:
                    bet_data["HomeTeamBet"] = bet["Bets"]["Spread"][1]
                    bet_data["AwayTeamBet"] = bet["Bets"]["Spread"][0]
        else:
            bet_data["HomeTeamBet"] = {"Team": hometeam, "Line": 0, "Odds": 0}
            bet_data["AwayTeamBet"] = {"Team": awayteam, "Line": 0, "Odds": 0}
        
        bet_data["BetType"] = "Spread"

        game_bets[game_key]["bets"].append(bet_data)

    return render_template('spread.html', box_items=game_bets.values(), active_view=active_view, current_date=start_of_day)

@app.route('/total', methods=['GET', 'POST'])
def total():
    active_view = 'Total'
    current_date = datetime.now().strftime('%Y-%m-%d')
    start_of_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)
    game_bets = {}
    for bet in Bets.objects(GameTime__gte=start_of_day, GameTime__lt=end_of_day):
        if bet['HomeTeam'] in TEAM_MAP:
            hometeam = TEAM_MAP[bet['HomeTeam']]
        else:
            hometeam = bet['HomeTeam']
        if bet['AwayTeam'] in TEAM_MAP:
            awayteam = TEAM_MAP[bet['AwayTeam']]
        else:
            awayteam = bet['AwayTeam']
        game_key = (hometeam, awayteam)
        if game_key not in game_bets:
            game_bets[game_key] = {'HomeTeam': hometeam, 'AwayTeam': awayteam, 'GameTime': bet['GameTime'].replace(tzinfo=utc).astimezone(est).strftime("%I:%M %p EST"), 'bets': []}
        game_bets[game_key]['bets'].append({
            'BetProvider': bet['BetProvider'],
            'HomeTeamBet': bet['Bets']['Total'][0],
            'AwayTeamBet': bet['Bets']['Total'][1],
            'BetType': 'Total'
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

@app.route('/record', methods=['GET', 'POST'])
def record():
    if request.method == "POST":
        team = request.form.get("team")
        team = TEAM_MAP[team]
    game_bets = {}    
    moneyline_filtered = {}
    total_filtered = {}
    spread_filtered = {}

    #filtering moneyline bets
    for bet in Bets.objects():   
        if bet["HomeTeam"] in TEAM_MAP:
            hometeam = TEAM_MAP[bet["HomeTeam"]]
        else:
            hometeam = bet["HomeTeam"]
        if bet["AwayTeam"] in TEAM_MAP:
            awayteam = TEAM_MAP[bet["AwayTeam"]]
        else:
            awayteam = bet["AwayTeam"]
        game_key = (hometeam, awayteam)
        if game_key not in game_bets:
            game_bets[game_key] = {
                "HomeTeam": hometeam,
                "AwayTeam": awayteam,
                "bets": [],
            }
        bet_data = {"BetProvider": bet["BetProvider"]}
        if "Bets" in bet and "Spread" in bet["Bets"] and len(bet["Bets"]["Spread"]) > 0:
            current_team = bet["Bets"]["Spread"][0]["Team"]
            # Convert the game_time from UTC to EST
            game_time = (bet["GameTime"].replace(tzinfo=utc).astimezone(est).strftime("%m/%d/%Y at %I:%M %p EST"
            ))
            game_bets[game_key]["GameTime"] = game_time
            if current_team not in TEAM_MAP:
                if current_team == hometeam:
                    bet_data["HomeTeamBet"] = bet["Bets"]["Spread"][0]
                    bet_data["AwayTeamBet"] = bet["Bets"]["Spread"][1]
                else:
                    bet_data["HomeTeamBet"] = bet["Bets"]["Spread"][1]
                    bet_data["AwayTeamBet"] = bet["Bets"]["Spread"][0]
            else:
                if TEAM_MAP[current_team] == hometeam:
                    bet_data["HomeTeamBet"] = bet["Bets"]["Spread"][0]
                    bet_data["AwayTeamBet"] = bet["Bets"]["Spread"][1]
                else:
                    bet_data["HomeTeamBet"] = bet["Bets"]["Spread"][1]
                    bet_data["AwayTeamBet"] = bet["Bets"]["Spread"][0]
        else:
            bet_data["HomeTeamBet"] = {"Team": hometeam, "Line": 0, "Odds": 0}
            bet_data["AwayTeamBet"] = {"Team": awayteam, "Line": 0, "Odds": 0}
        
        bet_data["BetType"] = "Spread"

        game_bets[game_key]["bets"].append(bet_data)
        

    for game_key, game_data in game_bets.items():
        if game_data["HomeTeam"] == team or game_data["AwayTeam"] == team:
            moneyline_filtered[game_key] = game_data

    #filtering total bets
    game_bets_tot = {}
    for bet in Bets.objects():   
        if bet["HomeTeam"] in TEAM_MAP:
            hometeam = TEAM_MAP[bet["HomeTeam"]]
        else:
            hometeam = bet["HomeTeam"]
        if bet["AwayTeam"] in TEAM_MAP:
            awayteam = TEAM_MAP[bet["AwayTeam"]]
        else:
            awayteam = bet["AwayTeam"]
        game_key = (hometeam, awayteam)
        if game_key not in game_bets_tot:
            game_bets_tot[game_key] = {
                "HomeTeam": hometeam,
                "AwayTeam": awayteam,
                "bets": [],
            }
        bet_data = {"BetProvider": bet["BetProvider"]}
        if "Bets" in bet and "Spread" in bet["Bets"] and len(bet["Bets"]["Spread"]) > 0:
            current_team = bet["Bets"]["Spread"][0]["Team"]
            # Convert the game_time from UTC to EST
            game_time = (bet["GameTime"].replace(tzinfo=utc).astimezone(est).strftime("%m/%d/%Y at %I:%M %p EST"
            ))
            game_bets_tot[game_key]["GameTime"] = game_time
            if current_team not in TEAM_MAP:
                if current_team == hometeam:
                    bet_data["HomeTeamBet"] = bet["Bets"]["Spread"][0]
                    bet_data["AwayTeamBet"] = bet["Bets"]["Spread"][1]
                else:
                    bet_data["HomeTeamBet"] = bet["Bets"]["Spread"][1]
                    bet_data["AwayTeamBet"] = bet["Bets"]["Spread"][0]
            else:
                if TEAM_MAP[current_team] == hometeam:
                    bet_data["HomeTeamBet"] = bet["Bets"]["Spread"][0]
                    bet_data["AwayTeamBet"] = bet["Bets"]["Spread"][1]
                else:
                    bet_data["HomeTeamBet"] = bet["Bets"]["Spread"][1]
                    bet_data["AwayTeamBet"] = bet["Bets"]["Spread"][0]
        else:
            bet_data["HomeTeamBet"] = {"Team": hometeam, "Line": 0, "Odds": 0}
            bet_data["AwayTeamBet"] = {"Team": awayteam, "Line": 0, "Odds": 0}
        
        bet_data["BetType"] = "Spread"

        game_bets_tot[game_key]["bets"].append(bet_data)

    for game_key, game_data in game_bets_tot.items():
        if game_data["HomeTeam"] == team or game_data["AwayTeam"] == team:
            total_filtered[game_key] = game_data

    #filtering through spread bets
    game_bets_spread = {}
    for bet in Bets.objects():   
        if bet["HomeTeam"] in TEAM_MAP:
            hometeam = TEAM_MAP[bet["HomeTeam"]]
        else:
            hometeam = bet["HomeTeam"]
        if bet["AwayTeam"] in TEAM_MAP:
            awayteam = TEAM_MAP[bet["AwayTeam"]]
        else:
            awayteam = bet["AwayTeam"]
        game_key = (hometeam, awayteam)
        if game_key not in game_bets_spread:
            game_bets_spread[game_key] = {
                "HomeTeam": hometeam,
                "AwayTeam": awayteam,
                "bets": [],
            }
        bet_data = {"BetProvider": bet["BetProvider"]}
        if "Bets" in bet and "Spread" in bet["Bets"] and len(bet["Bets"]["Spread"]) > 0:
            current_team = bet["Bets"]["Spread"][0]["Team"]
            # Convert the game_time from UTC to EST
            game_time = (bet["GameTime"].replace(tzinfo=utc).astimezone(est).strftime("%m/%d/%Y at %I:%M %p EST"
            ))
            game_bets_spread[game_key]["GameTime"] = game_time
            if current_team not in TEAM_MAP:
                if current_team == hometeam:
                    bet_data["HomeTeamBet"] = bet["Bets"]["Spread"][0]
                    bet_data["AwayTeamBet"] = bet["Bets"]["Spread"][1]
                else:
                    bet_data["HomeTeamBet"] = bet["Bets"]["Spread"][1]
                    bet_data["AwayTeamBet"] = bet["Bets"]["Spread"][0]
            else:
                if TEAM_MAP[current_team] == hometeam:
                    bet_data["HomeTeamBet"] = bet["Bets"]["Spread"][0]
                    bet_data["AwayTeamBet"] = bet["Bets"]["Spread"][1]
                else:
                    bet_data["HomeTeamBet"] = bet["Bets"]["Spread"][1]
                    bet_data["AwayTeamBet"] = bet["Bets"]["Spread"][0]
        else:
            bet_data["HomeTeamBet"] = {"Team": hometeam, "Line": 0, "Odds": 0}
            bet_data["AwayTeamBet"] = {"Team": awayteam, "Line": 0, "Odds": 0}
        
        bet_data["BetType"] = "Spread"

        game_bets_spread[game_key]["bets"].append(bet_data)

    for game_key, game_data in game_bets_spread.items():
        if game_data["HomeTeam"] == team or game_data["AwayTeam"] == team:
            spread_filtered[game_key] = game_data

    return render_template("record.html", team=team, moneyline=moneyline_filtered.values(), total=total_filtered.values(), spread=spread_filtered.values())
    

if __name__ == '__main__':
    load_bets()
    app.run(debug=True)
