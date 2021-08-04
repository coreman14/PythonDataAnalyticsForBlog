import requests
import json
import pandas as pd
import random
import csv
import os
from time import sleep
from tqdm import tqdm
from dataclasses import dataclass
import argparse
import matplotlib.pyplot as plt

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

def apiParse(zoneId,failcount,count,allzones,firstzone,zonecheck):
    first = True
    r = requests.get(f"https://api.weather.gov/zones/forecast/{zoneId}/observations")
    if r.status_code != 200:
        failcount += 1
        return failcount,count,allzones,firstzone,zonecheck
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
    return failcount,count,allzones,firstzone,zonecheck
    

        


def getDataFromAPI(ids): 
    zonecheck = True
    firstzone = [] #Weather history for the first zone
    allzones = [] #Current weather of all zones
    count = 0
    failcount = 0
    
    t = tqdm(ids,desc="APIS Called") #TQDM, For loop but with feedback
    
    for zoneId in t: 
        failcount,count,allzones,firstzone,zonecheck = apiParse(zoneId,failcount,count,allzones,firstzone,zonecheck)
        if len(firstzone) < 10:
            firstzone.clear()
            zonecheck = True
        if count > 9:
            t.set_description(f"Sleeping for 5 seconds, current failcount is {failcount}")
            sleep(5)
            t.set_description("APIS called")
            count = 0
        else:
            count +=1
            
    with open("WeatherDump/weatherall.csv","w+",newline='') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(weatherPoint.csvheader())
        for x in allzones:
            writer.writerow(x.csvout())
    with open("WeatherDump/weatherone.csv","w+",newline='') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(weatherPoint.csvheader())
        for x in firstzone:
            writer.writerow(x.csvout())
    print(f"Amount of api fails: {failcount}")
    return allzones,firstzone



def getDataFromFile():  # sourcery no-metrics
    firstzone = [] #Weather history for the first zone
    allzones = [] #Current weather of all zones 
    with open("WeatherDump/weatherall.csv","r") as f:
        reader = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        skip = False
        for row in reader:
            if not skip:#Skip the first row
                skip = True
                continue
            if len(row) == 0:
                continue #Skip any bad rows
            weather = weatherPoint(row[0],
                                   row[1],
                                   row[2],
                                   row[3])
            allzones.append(weather)

    with open("WeatherDump/weatherone.csv","r") as f:
        reader = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        skip  = False
        for row in reader:
            if not skip:#Skip the first row
                skip = True
                continue
            if len(row) == 0:
                continue #Skip any bad rows
            weather = weatherPoint(row[0],
                                   row[1],
                                   row[2],
                                   row[3])
            firstzone.append(weather)
    return allzones,firstzone


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
        print("Something went wrong, please try again.")
    for r in r.json()['features']:
        i = r.get('properties', None).get('id', None)
        if f"{STATE}Z" in i: #Checks if the item is a zone
            ids.append(i)


    if not os.path.exists("WeatherDump/weatherall.csv") or IGNORE_FILES:#only do this if we don't have a copy
        random.shuffle(ids) #Shuffle the id so that the first one is different everytime
        allzones,firstzone = getDataFromAPI(ids)
    else:
        allzones,firstzone = getDataFromFile()

if __name__ == "__main__":
    main()



