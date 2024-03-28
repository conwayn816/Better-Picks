from flask import Flask, render_template, redirect, url_for

Bets = [
    {
        "BetProvider": "Test Provider 1",
        "GameTime": "2024-04-01 12:00:00",
        "HomeTeam": "Home Team",
        "AwayTeam": "Away Team",
        "Bets": {
            "Spread": [
                {"Team": "Home Team", "Line": -3.5, "Odds": 100},
                {"Team": "Away Team", "Line": 3.5, "Odds": -100},
            ],
            "Total": [
                {"Team": "Over", "Line": 50.5, "Odds": 100},
                {"Team": "Under", "Line": 50.5, "Odds": -100},
            ],
            "Moneyline": [
                {"Team": "Home Team", "Odds": -110},
                {"Team": "Away Team", "Odds": 100},
            ],
        },
    },
    {
        "BetProvider": "Test Provider 2",
        "GameTime": "2024-04-01 12:00:00",
        "HomeTeam": "Home Team",
        "AwayTeam": "Away Team",
        "Bets": {
            "Spread": [
                {"Team": "Home Team", "Line": -4.5, "Odds": 100},
                {"Team": "Away Team", "Line": 4.5, "Odds": -100},
            ],
            "Total": [
                {"Team": "Over", "Line": 50.5, "Odds": 200},
                {"Team": "Under", "Line": 50.5, "Odds": -200},
            ],
            "Moneyline": [
                {"Team": "Home Team", "Odds": -100},
                {"Team": "Away Team", "Odds": -100},
            ],
        },
    },
    {
        "BetProvider": "Test Provide 4",
        "GameTime": "2024-04-01 12:00:00",
        "HomeTeam": "Home Team",
        "AwayTeam": "Away Team",
        "Bets": {
            "Spread": [
                {"Team": "Home Team", "Line": -3.5, "Odds": 100},
                {"Team": "Away Team", "Line": 3.5, "Odds": -100},
            ],
            "Total": [
                {"Team": "Over", "Line": 50.5, "Odds": 100},
                {"Team": "Under", "Line": 50.5, "Odds": -100},
            ],
            "Moneyline": [
                {"Team": "Home Team", "Odds": -110},
                {"Team": "Away Team", "Odds": 100},
            ],
        },
    },
    {
        "BetProvider": "Test Provider 3",
        "GameTime": "2024-04-01 12:00:00",
        "HomeTeam": "Home Team",
        "AwayTeam": "Away Team",
        "Bets": {
            "Spread": [
                {"Team": "Home Team", "Line": -4.5, "Odds": 100},
                {"Team": "Away Team", "Line": 4.5, "Odds": -100},
            ],
            "Total": [
                {"Team": "Over", "Line": 50.5, "Odds": 200},
                {"Team": "Under", "Line": 50.5, "Odds": -200},
            ],
            "Moneyline": [
                {"Team": "Home Team", "Odds": -100},
                {"Team": "Away Team", "Odds": -100},
            ],
        },
    },
]

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    active_view = 'Moneyline'
    moneyline_bets = [] 
    for bet in Bets:
        moneyline_bets.append({
            'BetProvider': bet['BetProvider'],
            'HomeTeamBet': bet['Bets']['Moneyline'][0],
            'AwayTeamBet': bet['Bets']['Moneyline'][1]
        })
        
    return render_template('index.html', title='Moneyline', box_items=moneyline_bets, active_view=active_view)

# NONFUNCTIONAL SWITCH VIEW
@app.route('/<view_name>', methods=['GET', 'POST'])
def switch_view(view_name):
    if view_name not in ['Spread', 'Total', 'Moneyline']:
        return redirect(url_for('index'))
    return render_template('index.html', **{'title': view_name, 'box_items': Bets[0]['Bets'][view_name]}, active_view=view_name)

if __name__ == '__main__':
    app.run(debug=True)