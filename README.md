# metadata_vs_waveform_data_at_IRIS
Make a list of all channel (net-sta-loc-chan) epochs for which meta-data is at the IRIS DMC but for which no waveforms were ever archived.  Covers all channels for CC,UO,UW.

Output is the sorted list of printed to screen as well as a simple text file named using the current date.

```
UW.ACES.--.ENE 2004-03-10T00:00:00 2004-03-10T00:00:01
UW.ACES.--.ENN 2004-03-10T00:00:00 2004-03-10T00:00:01
UW.ACES.--.ENZ 2004-03-10T00:00:00 2004-03-10T00:00:01
UW.ACES.--.HNE 2004-03-10T00:00:00 2004-03-10T00:00:01
UW.ACES.--.HNN 2004-03-10T00:00:00 2004-03-10T00:00:01
UW.ACES.--.HNZ 2004-03-10T00:00:00 2004-03-10T00:00:01
UW.ALCT.--.ENE 2004-02-28T00:00:00 2005-08-16T00:00:00
UW.ALCT.--.ENN 2004-02-28T00:00:00 2005-08-16T00:00:00
UW.ALCT.--.ENZ 2004-02-28T00:00:00 2005-08-16T00:00:00
UW.ASR.--.SHZ 1982-09-01T00:00:00 1982-09-30T00:00:00
...
```

This uses the IRIS metadata and availability webservices.

Example of metadata webservice output of (https://service.iris.edu/fdsnws/station/1/query?level=channel&network=CC,UO,UW&format=text): 
```
UW|ALKI||HNZ|47.5751|-122.4176|1|0|0|-90|NANOMETRICS|204000.0|1|m/s**2|200|2017-05-02T00:00:00|2020-08-05T19:50:15
UW|ALKI||HNZ|47.5751|-122.4176|1|0|0|-90|NANOMETRICS|204000.0|1|m/s**2|200|2020-08-05T19:50:15|
...
```

Example of availability webservice:
(http://service.iris.edu/fdsnws/availability/1/extent?format=text&net=UW,UO,CC&sta=ALKI&loc=--&cha=HNZ&orderby=nslc_time_quality_samplerate&includerestricted=false&starttime=2017-05-02T00:00:00.0000&endtime=2020-08-05T19:50:15.0000&nodata=404)
```
#Network Station Location Channel Quality SampleRate Earliest Latest Updated TimeSpans Restriction
UW ALKI -- HNZ M 200.0 2017-05-08T18:25:07.740000Z 2020-08-05T19:50:15.000000Z 2020-08-06T09:04:15Z 8579 OPEN
```
