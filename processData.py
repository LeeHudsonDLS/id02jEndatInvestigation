from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import os

EVENT_THRESHOLD_MAX = 0.002
EVENT_THRESHOLD_MIN = 0.001


class SnaptoCursor(object):
    def __init__(self, ax, x, y):
        self.ax = ax
        self.ly = ax.axvline(x = x[0],color='k', alpha=0.2)  # the vert line
        self.marker, = ax.plot(x[0],0,marker="o", color="crimson", zorder=3) 
        self.x = x
        self.y = y
        self.txt = ax.text(0.7, 0.9, '')

    def mouse_move(self, event):
        if not event.inaxes: return
        x, y = event.xdata, event.ydata
        indx = np.searchsorted(self.x, [x])[0]
        x = self.x[indx]
        y = self.y[indx]
        self.ly.set_xdata(x)
        self.marker.set_data([x],[y])
        self.txt.set_text('x=%s, y=%1.5f' % (mdates.num2date(x), y))
        self.txt.set_position((x,y))
        self.ax.figure.canvas.draw_idle()


# Method to convert datetime as a string to utc datetime
convertDate = lambda x: datetime.utcfromtimestamp(int(float(x)))

# Read out.csv
data = np.genfromtxt(f'{os.path.dirname(__file__)}/out.csv', 
                    delimiter=',', 
                    usecols=(0, 1, 2, 3),
                    converters={0:convertDate},
                    names=['time', 'endat', 'SSI', 'Diff'], 
                    dtype='datetime64[us], float, float, float')




fig, ax = plt.subplots()
lstDateTime = mdates.date2num(data['time'])


# Write poi.txt file
poiFound = False
poiFile = open(f'{os.path.dirname(__file__)}/poi.txt','w')
outString = ""
for index,event in enumerate(data['Diff']):
    if abs(event) > EVENT_THRESHOLD_MIN and abs(event) < EVENT_THRESHOLD_MAX:
        if not poiFound:
            poiFound = True
            t = data['time'][index]
            outString +=f'{t}\t{event}\n'
    else:
        poiFound = False

poiFile.write(outString)
poiFile.close()
    

# Cursor
endatCursor = SnaptoCursor(ax, lstDateTime, data['endat'])
ssiCursor = SnaptoCursor(ax, lstDateTime, data['SSI'])
diffCursor = SnaptoCursor(ax, lstDateTime, data['Diff'])
cid =  plt.connect('motion_notify_event', endatCursor.mouse_move)
cid =  plt.connect('motion_notify_event', ssiCursor.mouse_move)
cid =  plt.connect('motion_notify_event', diffCursor.mouse_move)

ax.plot(lstDateTime,data['endat'],color="blue",label='endat')
ax.plot(lstDateTime,data['SSI'],color="red",label='SSI')
ax.plot(lstDateTime,data['Diff'],color="green",label='Diff')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S.%f'))
fig.autofmt_xdate()


plt.ylabel('endat - ssi')
plt.legend()
#plt.axis([0, 1, -1, 1])

plt.show()
