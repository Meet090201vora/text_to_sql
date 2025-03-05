import requests

url = "http://localhost:8000/text-to-sql"
payload = {"user_query": "Names of all employees"}  # Ensure this is a dictionary
headers = {"Content-Type": "application/json"}  # Specify JSON content

response = requests.post(url, json=payload, headers=headers)
print(response.json())
