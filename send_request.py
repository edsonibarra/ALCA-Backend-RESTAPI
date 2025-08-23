import requests

url = "http://127.0.0.1:8000/api/houses-for-sale/"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU1OTc1Mzc4LCJpYXQiOjE3NTU5NzUwNzgsImp0aSI6IjNlN2VlNWVkYjQxODRjMzA4YWVlOTA0NTViM2VkMGZjIiwidXNlcl9pZCI6IjEifQ.hOApI1k2mlOpf-AEIq0vxL9f9bLFwHbgUQWAp-kLrf8"
}
response = requests.get(url, headers=headers)

print(response.json())