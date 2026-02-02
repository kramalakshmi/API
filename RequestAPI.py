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
  json_str = json.dumps(json_data, indent=4)
  print("Json put response body: " , json_str)

def post_req(user_id):
  data ={
    "name":"Naveen",
  "email": "naveen@auto.com",
  "gender":"Male",
  "status":"Inactive"
  }
  url = base_url+f"/public/v2/users"
  headers = {"Authorization" :auth_token}
  response = requests.post(url,json=data, headers= headers)
  assert response.status_code ==201
  json_data = response.json()
  json_str = json.dumps(json_data, indent=4)
  print("Json put response body: " , json_str)
  
def put_req(user_id):
  data ={
    "name":"Naveen",
  "email": "naveen@auto.com",
  "gender":"Male",
  "status":"Inactive"
  }
  url = base_url+f"/public/v2/users/{user_id}"
  headers = {"Authorization" :auth_token}
  response = requests.put(url,json=data, headers= headers)
  assert response.status_code ==200
  json_data = response.json()
  json_str = json.dumps(json_data, indent=4)
  print("Json put response body: " , json_str)

post_req()
get_req()
