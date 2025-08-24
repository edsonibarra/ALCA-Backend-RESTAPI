import requests

url = "http://127.0.0.1:8000/api/houses-for-sale/"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU1OTk1MTg5LCJpYXQiOjE3NTU5OTQ4ODksImp0aSI6IjdmZDBlNzQ2MDEyMDRkMzhhOTVlYjkwODE5Zjg4ZDc2IiwidXNlcl9pZCI6IjEifQ.1QQfJh4s0V4jcTzzPK7a1ZFa8yIEup-1f19Z3XXQRuE"
}
response = requests.get(url, headers=headers)

print(response.json())