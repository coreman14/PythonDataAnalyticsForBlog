import requests
import time
import json
tstart = time.time()
STATE = "MT"
ids = []
types = []
r = requests.get(f"https://api.weather.gov/zones?area={STATE}")
for r in r.json()['features']:
    ids.append(r.get('properties', None).get('id', None))

r = requests.get("https://api.weather.gov/products/types")

result = r.json()
for r in r.json()['@graph']:
    types.append(r.get('productCode', None))

print (len(types)) #As of july 23, 336 different types
with open("weatheroutput.txt",'w+') as w:
    for t in types:
        print(t)
        w.write(json.dumps(requests.get(f"https://api.weather.gov/zones/{t}/MTZ169/forecast").json()))
        w.write("\n\n")
        time.sleep(2)

print(f"This took {time.time() - tstart} to complete")#July 23, 709 seconds