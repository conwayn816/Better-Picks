import requests
import json

#double check and try with request headers

#these are response headers
headers = {
  'Accept' : 'application/json',
  'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'
}
'''
  'Access-Control-Allow-Credentials' : 'true',
  'Access-Control-Allow-Origin' : 'https://sportsbook.caesars.com',
  'Age' : '3',
  'Content-Encoding' : 'gzip',
  'Content-Type' : 'application/json',
  'Correlation-Id' : 'd040aa3d-82ec-48bd-8bd0-8243420d00d1',
  'Date' : 'Tue, 06 Feb 2024 21:02:43 GMT',
  'Vary' : 'origin,access-control-request-method,access-control-request-headers,accept-encoding',
  'Via' : '1.1 961ef6621cdae7a15d737e404049a1ec.cloudfront.net (CloudFront)',
  'X-Amz-Cf-Id' : 'qJa7dcTdyLYTM7MErehr80iXoOzEicsMROfbjEUp-NYFSNBTwVXmVg==',
  'X-Amz-Cf-Pop' : 'ATL59-P3',
  'X-Cache' :  'Hit from cloudfront',
  'X-Content-Type-Options' : 'nosniff ',
  'X-Envoy-Upstream-Service-Time' : '23'
'''

if __name__ == "__main__":
  url = "https://api.americanwagering.com/regions/us/locations/pa/brands/czr/sb/v3/cannedparlays/basketball"

  response = requests.get(url, headers=headers)
  flags = response.headers
  #print(flags)
  #print(response)
  
  if response.status_code == 200:
    data = response.json()
  else:
    print("Failed to retrieve")
    
    '''if data[0]["events"] in data[0]:
      print(data[0]["events"])

    print(data[0].get("collectionDisplayName"))
    '''
