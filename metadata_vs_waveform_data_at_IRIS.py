#!/usr/bin/env python

'''
https://tickets.pnsn.org/issues/4476
Make a list of all channels (net-sta-loc-chan) for which we have meta-data 
at the IRIS DMC but for which no waveforms were ever archived.

First get a list of all channels w net=UW.
Then for each NSLC, use the IRIS availabliity WS to see if any wiggle
data exist.  Use the 'extent' rather than 'query' since we just
want to know if any wiggle data were ever there.

Example of availability webservice:
http://service.iris.edu/fdsnws/availability/1/extent?format=text&net=UW&sta=HWK1&loc=--&cha=HNZ&orderby=nslc_time_quality_samplerate&includerestricted=false&nodata=404

Alex July 28, 2021
'''

import requests
import time
import datetime

nslc_yes_data = set()
nslc_no_data = set()
nslc_tried = set()
urlMD = "http://service.iris.edu/fdsnws/station/1/query?level=channel&network=UW&format=text"
request = requests.get(urlMD)

#---- sweep through all UW channels at IRIS
for line in request.text.splitlines():
    net = line.split('|')[0]
    sta = line.split('|')[1]
    loc = line.split('|')[2]
    if ( loc == "" ): loc = "--"
    cha = line.split('|')[3]
    nslc = net + '.' + sta + '.' + loc + '.' + cha
    if ( nslc not in nslc_tried ):
        nslc_tried.add(nslc)
        url_avail = "http://service.iris.edu/fdsnws/availability/1/extent?format=text&net=" + net + "&sta=" + sta + "&loc=" + loc + "&cha=" + cha + "&orderby=nslc_time_quality_samplerate&includerestricted=false&nodata=404"
#        print('Trying: ',nslc, url_avail)
        time.sleep(0.025)  # needed to avoid IRIS WS IPaddress 20sec-jail. Make it 0.05 if script is IRISWS barfing.
        #---- use the availability WS to check if wiggles present
        for line_avail in requests.get(url_avail).text.splitlines()[1:]:
            if ( "UW" in line_avail[0:2] ):
#                print("YES: ",nslc)
                nslc_yes_data.add(nslc)
                break
            else:
#                print("NO: ",nslc)
                nslc_no_data.add(nslc) 
                break

#---- write output
today = datetime.datetime.today()
todaystr = str(today.year) + '.' + str(today.month) + '.' + str(today.day)
fwrite = open('no_waveform_data_at_IRIS.' + todaystr,'w')
for nslc in sorted(nslc_no_data):
    fwrite.write(nslc + "\n")
    print(nslc)
fwrite.close()

