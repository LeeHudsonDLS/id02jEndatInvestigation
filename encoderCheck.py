from datetime import datetime
from turtle import st
from dateutil.relativedelta import relativedelta
import aa
import matplotlib.pyplot as plt
from numpy import append
import pytz


# Script to get data from the archiver for the ID02J axis 2 SSI encoder and test Endat encoder
# The script exports a CSV file with a common timestamp for each encoder to aid later analysis



# Return datetime objects over a given range
def date_range(start_date, end_date, increment, period):
    result = []
    nxt = start_date
    delta = relativedelta(**{period:increment})
    while nxt <= end_date:
        result.append(nxt)
        nxt += delta
    return result

# Create datetime objects for the start and finish of sampling
tz = pytz.timezone('Europe/London')
startTime = datetime(2021,6,9)
startTime=tz.localize(startTime).astimezone(pytz.utc)
finishTime = datetime(2022,4,20)
finishTime=tz.localize(finishTime).astimezone(pytz.utc)

endatEncoder = "SR02J-MO-AXIS-02:Y.RBV"
ssiEncoder = "SR02J-MO-SERVO-02:MOT.RBV"


# List of datetime objects for samples
times = date_range(startTime,finishTime,10,'minutes')

endatVals = list()
ssiVals = list()
diffVals = list()
poiVals = list()

poiTrigger = False

for time in times:
    endatVals.append(aa.get_value_at(endatEncoder,time).value[0])
    ssiVals.append(aa.get_value_at(ssiEncoder,time).value[0])
    diff = endatVals[-1]-ssiVals[-1]
    diffVals.append(diff)

# Write to csv
file = open("/home/jjc62351/work/id02j/out.csv","w")
for a in range(len(times)):
    file.write(f'{times[a].timestamp()},{endatVals[a]},{ssiVals[a]},{diffVals[a]}\n')
file.close()