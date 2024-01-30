#Andres
#https://sbapi.nj.sportsbook.fanduel.com/api/content-managed-page?page=CUSTOM&customPageId=nba&pbHorizontal=false&_ak=FhMFpcPWXMeyZxOx&timezone=America%2FNew_York

import requests

url = "https://sbapi.nj.sportsbook.fanduel.com/api/content-managed-page?page=CUSTOM&customPageId=nba&pbHorizontal=false&_ak=FhMFpcPWXMeyZxOx&timezone=America%2FNew_York"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
  
    moneylines = []

    if 'moneylines' in data:
        moneylines = data['moneylines']

    print("Moneylines:", moneylines)

else:
    print(f"Error Unable to Display Data: {response.status_code}")
