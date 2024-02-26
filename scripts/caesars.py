import requests
import json


def caesar_fetch(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        games = []
        for i in range(len(data['competitions'][0]['events'])):
            #getting strings for home/away teams
            games_dict = {}
            matchup = (data['competitions'][0]['events'][i]['name']).split()
            team1 = team2 = word = ""
            for itr in matchup:
                if itr == "|at|":
                    team1 = word
                    word = ""
                else:
                    word += " " + itr
            team2 = word
            team1 = team1[2:-1]
            team2 = team2[2:-1]
            games_dict['home_team'] = team2
            games_dict['away_team'] = team1
            #getting the spread, total, and moneyline values
            if len(data['competitions'][0]['events'][i]['markets']) > 0:
                spread = []
                moneyLine = []
                total = []
                #getting spread values
                odds = (data['competitions'][0]['events'][i]['markets'][1])
                #***W for winnings or payout
                awayW = odds['selections'][0]['price']['a']
                homeW = odds['selections'][1]['price']['a']
                #**S for spread
                homeS = odds['line']
                awayS = homeS * -1
                homeSpread = {}
                homeSpread['event'] = "NBA"
                homeSpread['type'] = "Spread"
                homeSpread['team'] = team2
                homeSpread['line'] = homeS
                homeSpread['odds'] = homeW
                spread.append(homeSpread)
                awaySpread = {}
                awaySpread['event'] = "NBA"
                awaySpread['type'] = "Spread"
                awaySpread['team'] = team1
                awaySpread['line'] = awayS
                awaySpread['odds'] = awayW
                spread.append(awaySpread)
                #getting total points values
                odds = (data['competitions'][0]['events'][i]['markets'][2])
                Over = odds['selections'][0]['price']['a']
                Under = odds['selections'][1]['price']['a']
                PO = odds['line']
                totalOver = {}
                totalOver['event'] = "NBA"
                totalOver['type'] = "Total"
                totalOver['team'] = "Over"
                totalOver['line'] = PO
                totalOver['odds'] = Over
                total.append(totalOver)
                totalUnder = {}
                totalUnder['event'] = "NBA"
                totalUnder['type'] = "Total"
                totalUnder['team'] = "Under"
                totalUnder['line'] = PO
                totalUnder['odds'] = Under
                total.append(totalUnder)
                #getting values for money line
                odds = (data['competitions'][0]['events'][i]['markets'][0]) 
                awayML = odds['selections'][0]['price']['a']
                homeML = odds['selections'][1]['price']['a']
                HOMEML = {}
                HOMEML['event'] = "NBA"
                HOMEML['type'] = "Moneyline"
                HOMEML['team'] = team2
                HOMEML['line'] = "N/A"
                HOMEML['odds'] = homeML
                moneyLine.append(HOMEML)
                AWAYML = {}
                AWAYML['event'] = "NBA"
                AWAYML['type'] = "Moneyline"
                AWAYML['team'] = team1
                AWAYML['line'] = "N/A"
                AWAYML['odds'] = awayML
                moneyLine.append(AWAYML)
                games_dict['bets'] = {"Spread": spread, "Total": total, "Moneyline": moneyLine}
                games.append(games_dict)

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data: {e}")
    return games

if __name__ == "__main__":
    #change this
    api_url = "https://api.americanwagering.com/regions/us/locations/pa/brands/czr/sb/v3/sports/basketball/events/schedule/?competitionIds=5806c896-4eec-4de1-874f-afed93114b8c"
    games = caesar_fetch(api_url)
