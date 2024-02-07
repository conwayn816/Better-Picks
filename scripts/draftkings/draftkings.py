import requests
import json


def extract_bets(data, bet_types):
    bets = []
    events = data['featuredDisplayGroup'].get('events', [])


    for offer_group in data['featuredDisplayGroup']['featuredSubcategories']:
        for event_group in offer_group.get('featuredEventGroupSubcategories', []):
            for offer_array in event_group.get('offers', []):
                for offer in offer_array:
                    # Ensure 'offer' is a dictionary and contains 'eventId' and 'label'
                    if isinstance(offer, dict) and 'eventId' in offer and 'label' in offer:
                        # Get the matchup for the current event

                        if offer['label'] in bet_types or offer['label'] == 'Total':
                            for outcome in offer['outcomes']:
                                current_team = outcome['participant']
                                # Determine if the bet is a team bet or an over/under bet
                                if offer['label'] == 'Total':
                                    # For Over/Under bets, use the label (Over/Under) as the team
                                    team = outcome['label']
                                else:
                                    # For other bets, use the participant as the team
                                    team = outcome['participant']

                                bets.append({
                                    'event': event_group['eventGroupName'],
                                    'type': offer['label'],
                                    'team': team,
                                    'line': outcome.get('line', 'N/A'),
                                    'odds': outcome['oddsAmerican']
                                })


    return bets

def organize_betting_data_ordered(bets):
    organized_games = []
    current_game = None

    for bet in bets:
        if bet['type'] == 'Spread':
            if current_game is None or len(current_game['bets']['Spread']) == 2:
                # Start a new game when no current game or both Spread bets have been added
                current_game = {
                    'home_team': bet['team'],  # First spread bet is the home team
                    'away_team': '',  # Placeholder for away team
                    'bets': {
                        'Spread': [bet],  # Add the first spread bet
                        'Total': [],  # Placeholder for total bets
                        'Moneyline': []  # Placeholder for moneyline bets
                    }
                }
                organized_games.append(current_game)
            else:
                # Second spread bet is the away team for the current game
                current_game['away_team'] = bet['team']
                current_game['bets']['Spread'].append(bet)
        elif bet['type'] == 'Total' and current_game is not None:
            # Add total bet to the current game
            current_game['bets']['Total'].append(bet)
        elif bet['type'] == 'Moneyline' and current_game is not None:
            # Add moneyline bet to the current game
            current_game['bets']['Moneyline'].append(bet)

    return organized_games





if __name__ == '__main__':
    url = 'https://sportsbook.draftkings.com/sites/US-SB/api/v4/featured/displaygroup/2/subcategories/4511/eventgroup/42648/gamelines?format=json'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        #print(data)

    else:
        print(f"Failed to retrieve data: {response.status_code}")

    bet_types = ['Moneyline', 'Spread']

    extracted_bets = extract_bets(data, bet_types)

    res = organize_betting_data_ordered(extracted_bets)
    prettified_json = json.dumps(res, indent=4)
    print(prettified_json)