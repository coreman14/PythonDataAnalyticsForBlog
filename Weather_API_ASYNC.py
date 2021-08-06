import requests
import json
import random
import csv
import os
from time import sleep
from tqdm import tqdm
from dataclasses import dataclass
import argparse
import asyncio
import httpx

def featureParse(i,zoneId):
    #split id into 2 parts Station and time
    time = i.get('id').replace('https://api.weather.gov/stations/',"")
    time = time.replace("/observations/","/").split("/")
    
    station = time[0]
    time = time[1]
    time = time.replace("T"," ").split("+")[0]
    
    props = i.get('properties')
    temp = props.get('temperature',"Not given").get('value',"Not given")
    if isinstance(temp,tuple):
        temp = temp[0]
    return weatherPoint(zoneId, time, station, temp if temp is not None else "Not given")


def apiParseasync(zoneId,failcount,allzones,firstzone,zonecheck,r):
    first = True
    try:
        if r.status_code != 200:
            failcount += 1
            return failcount,allzones,firstzone,zonecheck
    except:
        failcount += 1
        return failcount,allzones,firstzone,zonecheck
    with open(f"WeatherDump/{zoneId}response.json","w+") as j:
        json.dump(r.json(),j)
        
    for i in r.json()['features']:
        weather = featureParse(i,zoneId)
        if first:
            allzones.append(weather)#used for compareing current temps
            first = False
        if zonecheck:#if we are doing the first zone, append all
            firstzone.append(weather)
        else:#Else only get first one
            break
    zonecheck = False
    return failcount,allzones,firstzone,zonecheck

async def getDataFromAPIasync(ids): 
    zonecheck = True
    firstzone = [] #Weather history for the first zone
    allzones = [] #Current weather of all zones
    count = 0
    failcount = 0
    
    
    async with httpx.AsyncClient() as client:
        tasks = (client.get(f"https://api.weather.gov/zones/forecast/{zoneId}/observations") for zoneId in ids)
        reqs = await asyncio.gather(*tasks,return_exceptions=True)
    
    reqs = zip(ids,reqs)
    t = tqdm(reqs,desc="APIS Called") #TQDM, For loop but with feedback
    for zoneId,r in t: 
        failcount,allzones,firstzone,zonecheck = apiParseasync(zoneId,failcount,allzones,firstzone,zonecheck,r)
        if len(firstzone) < 10:
            firstzone.clear()
            zonecheck = True

            
    # with open("WeatherDump/weatherall.csv","w+",newline='') as f:
    #     writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #     writer.writerow(weatherPoint.csvheader())
    #     for x in allzones:
    #         writer.writerow(x.csvout())
    # with open("WeatherDump/weatherone.csv","w+",newline='') as f:
    #     writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #     writer.writerow(weatherPoint.csvheader())
    #     for x in firstzone:
    #         writer.writerow(x.csvout())
    print(f"Amount of api fails: {failcount}")

@dataclass(frozen=True)
class weatherPoint:
    Zone: str
    Time: str
    Station: str
    Temp: float
    
    def csvout(self):
        return [self.Zone,
                self.Time,
                self.Station,
                self.Temp]
    @staticmethod
    def csvheader():
        return["Zone",
                "Time",
                "Station",
                "Temp"]

def main():
    parser = argparse.ArgumentParser("Use the free USA weather api to plot current data of a state(Default montana)")
    parser.add_argument("-s","--state",type=str,help="Change the state to get data from(Default is montana)")
    parser.add_argument("-f","--force",action="store_true",help="Force running of api")
    args = parser.parse_args()
    STATE = "MT" if args.state is None else args.state
    IGNORE_FILES = True if not args.force else args.force
    ids = [] #IDs for weather station

    r = requests.get(f"https://api.weather.gov/zones?area={STATE}")
    if r.status_code == 400:
        print(f"{STATE} is not a valid state. ")
        exit(0)
    elif r.status_code >= 401:
        print(f"Something went wrong, please try again. {r.status_code = }")
    for r in r.json()['features']:
        i = r.get('properties', None).get('id', None)
        if f"{STATE}Z" in i: #Checks if the item is a zone
            ids.append(i)


    if not os.path.exists("WeatherDump/weatherall.csv") or IGNORE_FILES:#only do this if we don't have a copy
        random.shuffle(ids) #Shuffle the id so that the first one is different everytime
        asyncio.run(getDataFromAPIasync(ids))


if __name__ == "__main__":
    main()



