with open("WeatherDump/weatherone.csv","r") as f:
    j = f.readlines()
with open("WeatherDump/weatherone.csv","w+") as f:
    for x in j:
        if x == "\n":
            continue
        f.write(x)