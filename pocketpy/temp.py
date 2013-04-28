import json
from jsonconfig import JsonConfig


CONFIG_FILE = 'a.txt'
jc = JsonConfig(CONFIG_FILE)
print jc.read()
jc.config = {'consumer_key': 'ttttttttt', 'access_token': 'yyyyyyyy'}
jc.save()
print jc.read()


a={'1':"11",'2':"22"}
for tt in a:
    print tt,"===",a[tt]
