import json
import urllib.request
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import matplotlib.dates as mdates
from clyent import color

oldData=[]

def incorrectStatsFile():
    if ['y', 'Y'].__contains__(input("Stats file incorrect, overwrite?(Y/n) ")):
        global oldData
        oldData=[]
    else:
        exit()

url = urllib.request.urlopen("https://www.wp.pl/v1/covid")
newData=json.loads(url.read())

try:
    with open('covidstats.json', 'r') as f:
        oldData=json.loads(f.read())
        if type(oldData)!=list:
            raise ValueError
except FileNotFoundError:
    print("Stats file not found, creating new file")
except json.decoder.JSONDecodeError:
    incorrectStatsFile()
except ValueError:
    incorrectStatsFile()

for i in newData.get('cases'):
    if oldData.__contains__(i)==False:
        oldData.append(i)

with open('covidstats.json', 'w') as f:
    f.write(json.dumps(oldData))

with open('covidstats.csv', 'w') as f:
    for i in oldData[0].keys():
        f.write(i)
        f.write(',')
    f.write('\n')
    for x in oldData:
        for y in x.values():
            f.write(str(y))
            f.write(',')
        f.write('\n')
        
print ("Today's new cases: " + str(oldData[-1].get("newCases")))
print ("Today's deaths: " +str(oldData[-1].get("newDeaths")))

if ['y', 'Y'].__contains__(input("Do you want to see graphs?(Y/n) ")):
    dates=[]
    cases=[]
    deaths=[]
    for i in oldData:
        dates.append(dt.date.fromisoformat(i.get("date")))
        cases.append(i.get("newCases"))
        deaths.append(i.get("newDeaths"))

    plt.plot(dates, cases, color="red")
    plt.xticks(ticks=dates[0::int(np.floor(len(dates)/4))])
    plt.ylabel("New cases")
    plt.title("New cases")
    plt.show()

    plt.plot(dates,deaths, color="black")
    plt.xticks(ticks=dates[0::int(np.floor(len(dates)/4))])
    plt.ylabel("Deaths")
    plt.title("Deaths")
    plt.show()
else:
    exit()