import requests

url = "https://emsiservices.com/skills/versions/latest/changes"

headers = {"Authorization": "Bearer <ACCESS_TOKEN>"}

response = requests.request("GET", url, headers=headers)

print(response.text)