from flask import Flask, render_template, redirect, url_for

# TEMP DATABASE FOR TESTING
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

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('moneyline'))

@app.route('/moneyline', methods=['GET', 'POST'])
def moneyline():
    active_view = 'Moneyline'
    game_bets = {}
    for bet in Bets:
        game_key = (bet['HomeTeam'], bet['AwayTeam'])
        if game_key not in game_bets:
            game_bets[game_key] = {'HomeTeam': bet['HomeTeam'], 'AwayTeam': bet['AwayTeam'], 'bets': []}
        game_bets[game_key]['bets'].append({
            'BetProvider': bet['BetProvider'],
            'HomeTeamBet': bet['Bets']['Moneyline'][0],
            'AwayTeamBet': bet['Bets']['Moneyline'][1]
        })
    return render_template('moneyline.html', box_items=game_bets.values(), active_view=active_view)

@app.route('/spread', methods=['GET', 'POST'])
def spread():
    active_view = 'Spread'
    game_bets = {}
    for bet in Bets:
        game_key = (bet['HomeTeam'], bet['AwayTeam'])
        if game_key not in game_bets:
            game_bets[game_key] = {'HomeTeam': bet['HomeTeam'], 'AwayTeam': bet['AwayTeam'], 'bets': []}
        game_bets[game_key]['bets'].append({
            'BetProvider': bet['BetProvider'],
            'HomeTeamBet': bet['Bets']['Spread'][0],
            'AwayTeamBet': bet['Bets']['Spread'][1]
        })
    return render_template('spread.html', box_items=game_bets.values(), active_view=active_view)

@app.route('/total', methods=['GET', 'POST'])
def total():
    active_view = 'Total'
    game_bets = {}
    for bet in Bets:
        game_key = (bet['HomeTeam'], bet['AwayTeam'])
        if game_key not in game_bets:
            game_bets[game_key] = {'HomeTeam': bet['HomeTeam'], 'AwayTeam': bet['AwayTeam'], 'bets': []}
        game_bets[game_key]['bets'].append({
            'BetProvider': bet['BetProvider'],
            'HomeTeamBet': bet['Bets']['Total'][0],
            'AwayTeamBet': bet['Bets']['Total'][1]
        })
    return render_template('total.html', box_items=game_bets.values(), active_view=active_view)

if __name__ == '__main__':
    app.run(debug=True)