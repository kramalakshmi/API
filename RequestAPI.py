import requests
import json

base_url ="https://gorest.co.in"
#Auth token
auth_token = "Bearer d5fc969f6b60ddb68552800e3cdf7bf384b2489372ee15c773445b658000f405"

def get_req():
  url = base_url+"/public/v2/users/"
  headers = {"Authorization" :auth_token}
  response = requests.get(url, headers= headers)
  assert response.status_code ==200
  json_data = response.json()
  print("Json response body: "+ str(json_data))

get_req()
