# Nate
import requests





if __name__ == "__main__":
    url = 'https://sports.tn.betmgm.com/en/sports/api/widget/widgetdata?layoutSize=Small& page=CompetitionLobby&sportId=7&regionId=9&competitionId=6004&compoundCompetitionId=1:6004&widgetId=/mobilesports-v1.0/layout/layout_us/modules/basketball/nba/nba-gamelines-complobby&shouldIncludePayload=true'

    response = requests.get(url)   

    if response.status_code == 200:
        print(response.json())
    else:
        print("Error: " + str(response.status_code))

    
    


