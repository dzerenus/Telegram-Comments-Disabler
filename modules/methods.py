import json
import requests
from time import sleep
from requests.exceptions import ConnectionError 


def post(url, headers={}, data={}):
	is_sended = False
	res = None

	while not is_sended:
		try:
			req = requests.post(url=url, headers=headers, data=json.dumps(data))
			is_sended = True
			res = req.json()
			return res

		except ConnectionError:
			print("Connection error!")
			sleep(1)