# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 13:15:05 2021

@author: andre
"""

import matplotlib.pyplot as plt
import numpy as np
import csv

    #0"LAP_BEACON",
    #1"G_LAT",
    #2"ROTY",
    #3"STEERANGLE",
    #4"SPEED",
    #5"THROTTLE",
    #6"BRAKE",
    #7"GEAR",
    #8"G_LON",
    #9"CLUTCH",
    #10"RPMS",
    #11"TC",
    #12"ABS",
    #13"SUS_TRAVEL_LF",
    #14"SUS_TRAVEL_RF",
    #15"SUS_TRAVEL_LR",
    #16"SUS_TRAVEL_RR",
    #17"BRAKE_TEMP_LF",
    #18"BRAKE_TEMP_RF",
    #19"BRAKE_TEMP_LR",
    #20"BRAKE_TEMP_RR",
    #21"TYRE_PRESS_LF",
    #22"TYRE_PRESS_RF",
    #23"TYRE_PRESS_LR",
    #24"TYRE_PRESS_RR",
    #25"TYRE_TAIR_LF",
    #26"TYRE_TAIR_RF",
    #27"TYRE_TAIR_LR",
    #28"TYRE_TAIR_RR",
    #29"WHEEL_SPEED_LF",
    #30"WHEEL_SPEED_RF",
    #31"WHEEL_SPEED_LR",
    #32"WHEEL_SPEED_RR",
    #33"BUMPSTOPUP_RIDE_LF",
    #34"BUMPSTOPUP_RIDE_RF",
    #35"BUMPSTOPUP_RIDE_LR",
    #36"BUMPSTOPUP_RIDE_RR"


## Auslesen der Geschwindigkeit
# with open('motecdata01.csv') as csvdatei: 
#     csv_reader_object = csv.reader(csvdatei)   
#     speed=np.arange(0)   
#     zeilennummer=1
#     for row in csv_reader_object:
#         if zeilennummer ==9:
#             print(row[0],row[1],row[2])
#             samplerate=row[1]
#         elif zeilennummer >=19:
#             speed = np.append(speed, [row[4]])
#         zeilennummer=zeilennummer+1
# samplerate = np.asfarray(samplerate,float)
# speed=np.asfarray(speed,float)
# x=np.arange(0,zeilennummer-19)/samplerate
# speedms=speed/3.6



###Auslesen G_Lat G_lon
with open('motecdata01.csv') as csvdatei: 
    csv_reader_object = csv.reader(csvdatei)   
    g_lon=np.arange(0)
    g_lat=np.arange(0) 
    speed=np.arange(0)
    zeilennummer=1
    for row in csv_reader_object:
        if zeilennummer ==9:
            print(row[0],row[1],row[2])
            samplerate=row[1]
        elif zeilennummer >=19:
            speed=np.append(speed,row[4])
            g_lat = np.append(g_lat, [row[1]])
            g_lon = np.append(g_lon, [row[8]])
        zeilennummer=zeilennummer+1
samplerate = np.asfarray(samplerate,float)
time=np.arange(0,zeilennummer-19)/samplerate


x=np.asfarray(time,float)
y=np.asfarray(speed,float)/3.6
g_lat=np.asfarray(g_lat,float)
g_lon=np.asfarray(g_lon,float)


a_diff=[0.0]*len(time)
for i in range(len(speed)-1):
    a_diff[i]=(y[i+1]-y[i])/(x[i+1]-x[i])
a_diff[-1]=(y[-1]-y[-2])/(x[-1]-x[-2])

dt=0
x1=0
x2=0
a=y.copy()
a_soft=y.copy()
for i in range(len(a)-1):
    x1+=1
    if a[i]!=a[i+1]:
        dt=x1-x2
        for j in range(x2,x1):
            a_soft[j]=(a[i+1]-a[i])*samplerate/9.81/(x1-x2)
        a_soft[-1]=(a[-1]-a[-2])*samplerate/9.81/(x1-x2)    
        x2=x1
a_soft[-1]=0        
a_soft[-2]=0        
a_soft[-3]=0        
a_soft[-4]=0        
        
# plt.plot(x,a_diff)
# plt.plot(x[:500],a_soft[:500])



## Scatter Histogramm
def scatter_hist(x, y, ax, ax_histx, ax_histy):
    # no labels
    ax_histx.tick_params(axis="x", labelbottom=False)
    ax_histy.tick_params(axis="y", labelleft=False)

    # the scatter plot:
    ax.scatter(x, y)

    # now determine nice limits by hand:
    binwidth = 0.25
    xymax = max(np.max(np.abs(x)), np.max(np.abs(y)))
    lim = (int(xymax/binwidth) + 1) * binwidth

    bins = np.arange(-lim, lim + binwidth, binwidth)
    ax_histx.hist(x, bins=bins)
    ax_histy.hist(y, bins=bins, orientation='horizontal')

# definitions for the axes
left, width = 0.1, 0.65
bottom, height = 0.1, 0.65
spacing = 0.005


rect_scatter = [left, bottom, width, height]
rect_histx = [left, bottom + height + spacing, width, 0.2]
rect_histy = [left + width + spacing, bottom, 0.2, height]

# start with a square Figure
fig = plt.figure(figsize=(8, 8))

ax = fig.add_axes(rect_scatter)
ax_histx = fig.add_axes(rect_histx, sharex=ax)
ax_histy = fig.add_axes(rect_histy, sharey=ax)

# use the previously defined function
scatter_hist(g_lat,a_soft, ax, ax_histx, ax_histy)

plt.show()




# ### Berechnung Beschleunigung Längs
# dspeedms=[0.0]*len(speedms)
# for i in range(len(speedms)-1):    
#     dspeedms[i]=(speedms[i+1]-speedms[i])/(x[i+1]-x[i])
# dspeedms[-1]=(speedms[-1]-speedms[-2])/(x[-1]-x[-2])

# glong=np.asfarray(dspeedms,float)/9.81




