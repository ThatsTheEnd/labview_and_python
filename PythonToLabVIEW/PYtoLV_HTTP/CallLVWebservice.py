import requests
x = 5
y = 10
url = f"http://127.0.0.1:9090/Math-WebServer/Add?y={y}&x={x}"
response = requests.get(url)
print(response.text)
