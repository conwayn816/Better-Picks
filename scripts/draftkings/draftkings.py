import requests


def extract_bets(data, bet_types):
    bets = []
    events = data['featuredDisplayGroup'].get('events', [])

    # Create a dictionary to map event IDs to matchups
    event_matchups = {
        event['eventId']: f"{event['teamName1']} vs {event['teamName2']}"
        for event in events
    }

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
                                print('CURRENT TEAM: ', current_team)
                                # Determine if the bet is a team bet or an over/under bet
                                if offer['label'] == 'Total':
                                    # For Over/Under bets, use the label (Over/Under) as the team
                                    team = current_team
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
                                print(bets[:-1])

    return bets








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


    for bet in extracted_bets:
        print(bet)