import requests
import json
import re
import math

# Function to get the bets
def getBets(data):
    # Create an empty list to save the bets
    bets = []

    # Loop through the events
    for event in data['events']:

        # Check if the event is an NBA event
        if "NBA" in event['competitionName']:

            # Check if the home team and away team are not empty
            if event['homeTeam'] == '' or event['awayTeam'] == '':
                continue

            # Create a dictionary to save the bet types
            bet_types = {}

            # Loop through the specialFixedOddsMarkets to find bet types
            for types in event['specialFixedOddsMarkets']:

                # Check if the bet type is Moneyline, Point Spread or Total
                if types['eventName'] == "Moneyline" or types['eventName'] == "Point Spread" or types['eventName'] == "Total":

                    # Change the bet type name to Spread if it is Point Spread
                    if types['eventName'] == "Point Spread":
                        types['eventName'] = "Spread"

                    # Save the start time of the event
                    types['startTime'] = types['advertisedStartTime'].replace("T", " ").replace("Z", "")

                    # Save the bet types to the bet_types dictionary
                    bet_type = types['eventName']
                    bet_type_data = []

                    # Loop through the outcomes to get the team, line and odds
                    for outcomes in types['outcomes']:
                        pattern = r'[-+]?\d*\.\d+|\d+'
                        numerical_value = re.findall(pattern, outcomes['name'])
                        if outcomes['price'] < 2.00:
                            odds = str(-math.ceil(((100 / (outcomes['price'] - 1)) / 5.01)) * 5)
                        else:
                            odds = str(+math.ceil((((outcomes['price'] - 1) * 100) / 5.01)) * 5)

                        # Check if the bet type is Moneyline
                        if types['eventName'] == "Moneyline":
                            team_name = event['homeTeam'] if outcomes['name'].startswith(event['homeTeam']) else event['awayTeam']
                            if '-' not in odds:
                                odds = "+" + odds 
                            bet_type_data.append({
                                'event': "NBA",
                                'type': types['eventName'],
                                'team': team_name,
                                'line': "N/A",
                                'odds': odds,
                            })
                        else:
                            team_name = "Over" if "Over" in outcomes['name'] else "Under" if "Under" in outcomes['name'] else event['homeTeam'] if outcomes['name'].startswith(event['homeTeam']) else event['awayTeam']
                            bet_type_data.append({
                                'event': "NBA",
                                'type': types['eventName'],
                                'team': team_name,
                                'line': float(numerical_value[0]),
                                'odds': odds,
                            })
                    bet_types[bet_type] = bet_type_data
                    
            # Save the bets
            bets.append({
                'home_team': event['homeTeam'],
                'away_team': event['awayTeam'],
                'start_time': types['startTime'],
                'bets': bet_types
            })
    return bets