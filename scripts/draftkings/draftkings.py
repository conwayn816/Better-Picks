import requests
import json
from datetime import datetime

def parse_date(date_string):
    date_string = date_string.rstrip('Z')
    if '.' in date_string:
        date_string_parts = date_string.split('.')
        date_string = date_string_parts[0] + '.' + date_string_parts[1][:6]
    date_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%f")
    return date_object.isoformat() + 'Z'

def extract_bets(data, bet_types):
    bets = []
    for offer_group in data['featuredDisplayGroup']['featuredSubcategories']:
        for event_group in offer_group.get('featuredEventGroupSubcategories', []):
            for offer_array in event_group.get('offers', []):
                for offer in offer_array:
                    # Ensure 'offer' is a dictionary and contains 'eventId' and 'label'
                    if isinstance(offer, dict) and 'eventId' in offer and 'label' in offer:
                        # Get the matchup for the current event
                        eventId = offer['eventId']
                        if offer['label'] in bet_types or offer['label'] == 'Total':
                            for outcome in offer['outcomes']:
                                current_team = outcome.get('participant', outcome.get('label', 'Unknown'))
                                # Determine if the bet is a team bet or an over/under bet
                                if offer['label'] == 'Total':
                                    # For Over/Under bets, use the label (Over/Under) as the team
                                    team = outcome['label']
                                else:
                                    # For other bets, use the participant as the team
                                    team = outcome.get('participant', 'Unknown')

                                bets.append({
                                    'event': event_group['eventGroupName'],
                                    'eventId': eventId,
                                    'type': offer['label'],
                                    'team': team,
                                    'line': outcome.get('line', 'N/A'),
                                    'odds': outcome.get('oddsAmerican', 'N/A'),
                                })


    return bets

def organize_betting_data_ordered(bets, event_start_dates):
    organized_games = []
    current_game = None

    for bet in bets:
        if bet['type'] == 'Spread':
            if current_game is None or len(current_game['bets']['Spread']) == 2:
                game_start_date = parse_date(event_start_dates[bet['eventId']]) if bet['eventId'] in event_start_dates else 'Unknown date'
                # Start a new game when no current game or both Spread bets have been added
                current_game = {
                    'BetProvider': 'DraftKings',
                    'home_team': '',  # First spread bet is the away team
                    'away_team': bet['team'],  # Placeholder for home team
                    'GameTime': game_start_date,
                    'bets': {
                        'Spread': [bet],  # Add the first spread bet
                        'Total': [],  # Placeholder for total bets
                        'Moneyline': []  # Placeholder for moneyline bets
                    }
                }
                organized_games.append(current_game)
            else:
                # Second spread bet is the away team for the current game
                current_game['home_team'] = bet['team']
                current_game['bets']['Spread'].append(bet)
        elif bet['type'] == 'Total' and current_game is not None:
            # Add total bet to the current game
            current_game['bets']['Total'].append(bet)
        elif bet['type'] == 'Moneyline' and current_game is not None:
            current_game['bets']['Moneyline'].append(bet)

    return organized_games





