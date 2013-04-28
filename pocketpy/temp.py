import json
from jsonconfig import JsonConfig


CONFIG_FILE = 'a.txt'
jc = JsonConfig(CONFIG_FILE)
jc.config = {'consumer_key': 'ttttttttt', 'access_token': 'yyyyyyyy'}
jc.save()
print jc.read()
