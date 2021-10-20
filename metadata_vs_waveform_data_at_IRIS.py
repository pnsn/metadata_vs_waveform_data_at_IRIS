#!/usr/bin/env python

'''
https://tickets.pnsn.org/issues/4476
Make a list of all channel epochs (net-sta-loc-chan T1 T2) for which we have meta-data 
at the IRIS DMC but for which no waveforms were ever archived.

First get a list of all channels w net=UW.
Then for each NSLC, use the IRIS availabliity WS to see if any wiggle
data exist.  Use the 'extent' rather than 'query' since we just
want to know if any wiggle data were ever there.

Example of metadata webservice output of https://service.iris.edu/fdsnws/station/1/query?level=channel&network=UW&format=text: 
UW|ALKI||HNZ|47.5751|-122.4176|1|0|0|-90|NANOMETRICS|204000.0|1|m/s**2|200|2017-05-02T00:00:00|2020-08-05T19:50:15
UW|ALKI||HNZ|47.5751|-122.4176|1|0|0|-90|NANOMETRICS|204000.0|1|m/s**2|200|2020-08-05T19:50:15|

Example of availability webservice:
http://service.iris.edu/fdsnws/availability/1/extent?format=text&net=CC,UO,UW&sta=ALKI&loc=--&cha=HNZ&orderby=nslc_time_quality_samplerate&includerestricted=false&starttime=2017-05-02T00:00:00.0000&endtime=2020-08-05T19:50:15.0000&nodata=404

Alex Oct 19, 2021
'''

import requests
import time
import datetime

nslc_yes_data = set()
nslc_no_data = set()
nslc_tried = set()
urlMD = "http://service.iris.edu/fdsnws/station/1/query?level=channel&network=CC,UO,UW&format=text"
request = requests.get(urlMD)
now = datetime.datetime.now()
Tnow = now.strftime("%Y-%m-%dT%H:%M:%S")

#---- sweep through all UW channel epochs at IRIS
for line in request.text.splitlines():
  if ( "#" not in line ):
    net = line.split('|')[0]
    sta = line.split('|')[1]
    loc = line.split('|')[2]
    if ( loc == "" ): loc = "--"
    cha = line.split('|')[3]
    nslc = net + '.' + sta + '.' + loc + '.' + cha
    T1 = line.split('|')[15]
    try:
        T2 = line.split('|')[16]
    except:
        T2 = "2599-01-01T00:00:00"
    T1 = T1.split('.')[0]
    T2 = T2.split('.')[0]
    if ( len(T2) < 10 ): T2 = "2599-01-01T00:00:00"
    url_avail = "http://service.iris.edu/fdsnws/availability/1/extent?format=text&net=" + net + "&sta=" + sta + "&loc=" + loc + "&cha=" + cha + "&orderby=nslc_time_quality_samplerate&includerestricted=false&starttime=" + T1 + "&endtime=" + T2 + "&nodata=404"
    time.sleep(0.025)  # needed to avoid IRIS WS IPaddress 20sec-jail. Make it 0.05 if script is IRISWS barfing.
    #---- use the availability WS to check if wiggles present
    for line_avail in requests.get(url_avail).text.splitlines()[1:]:
        if ( net in line_avail[0:2] and sta in line_avail[3:8] ):
            nslc_yes_data.add(nslc)
            break
        else:
            linewrite = nslc + " " + T1 + " " + T2
            nslc_no_data.add(linewrite)
            break

#---- write output
today = datetime.datetime.today()
todaystr = str(today.year) + '.' + str(today.month) + '.' + str(today.day)
fwrite = open('no_waveform_data_at_IRIS.' + todaystr,'w')
for nslc in sorted(nslc_no_data):
    fwrite.write(nslc + "\n")
    print(nslc)
fwrite.close()

