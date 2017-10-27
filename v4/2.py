import requests

response = requests.get("https://github.com/favicon.ico")
with open('favicon.ico','wb') as f:
	f.write(response.content)
	f.close()