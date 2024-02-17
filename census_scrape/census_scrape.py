import requests
from pprint import pprint

url = ""
# let library handle URL parameters
params = {"search": "distribution_pattern:nationwide",
          "limit": 2}

response = requests.get(url, params)
# response objects have built in .json() method for decoding
pprint(response.json())