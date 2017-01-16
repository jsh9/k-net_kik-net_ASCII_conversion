# K-net/KiK-net ASCII conversion
#### Converts K-NET or KiK-net raw ASCII data files into usable ASCII waveforms

## Description
The original ASCII data format from the K-NET and KiK-net database (http://www.kyoshin.bosai.go.jp/) is very cumbersome to use. This module can convert the original data format into ready-to-use 2-column waveform format (i.e., 1st column = time, 2nd column = ground acceleration).

## How to use this module

1. Download seismograms from K/Kik-net website to the hard drive, and arrange the folders in the following fashion:
  ```
    [FKSH14] 
    
      | [FKSH140101041318]
      | [FKSH140101190811]
      | [FKSH140102050417]
      | [FKSH140102250654]
      | [FKSH140102261508]
      |
      ...
  ```
  Namely, use the seismic station name (e.g., "FKSH14") as the parent folder name, and at this seismic station, each recorded earthquake has its own folder (e.g., "FKSH140101041318"), where the raw ASCII-format data files are stored.
  
2. Put `kyoshin_bosai.py` into Python search path

3. To convert only one earthquake (or "event"), use
    ```Python
    import kyoshin_bosai
    parent_folder = './FKSH14'
    event_name = 'FKSH140101041318'
    station_type = 'kik'  # FKSH14 is a Kik-net station; for K-NET stations, use 'k'
    kyoshin_bosai.convert_single_event(parent_folder,event_name,station_type)
    ```
4. To convert all the earthquake at a station, use
    ```Python
    import kyoshin_bosai
    parent_folder = './FKSH14'
    kyoshin_bosai.convert_multiple_events(parent_folder)
    ```
    
## Output files
For Kik-net stations, the output files are:
```
FKSH140101041318.basic_info.txt
FKSH140101041318.EW1.txt
FKSH140101041318.EW2.txt
FKSH140101041318.NS1.txt
FKSH140101041318.NS2.txt
FKSH140101041318.UD1.txt
FKSH140101041318.UD2.txt
```
where `EW`, `NS`, and `UD` designate east-west, north-south, and vertical directions, respectively; and `1` and `2` designate downhole seismometer and ground-surface seismometer, respectively. `FKSH140101041318` is the event name, and is different for different earthquakes.

`[event_name].basic_info.txt` contains basic information for the earthquake. Below is an example:

```
Station_Name	KSRH10
Station_Lat	43.2084
Station_Lon	145.1168
Origin_Date	2003/09/26
Origin_Time	04:50:00
Rec_Start_Date	2003/09/26
Rec_Start_Time	04:50:38
Duration_Time(s)	300
Last_Corr_Date	2003/09/26
Last_Corr_Time	04:00:00
EQ_Lat	41.781
EQ_Lon	144.074
EQ_Mag	8.0
EQ_Depth(km)	42
Samp_Freq(Hz)	200
Surf_Height(m)	31
PGA_EW2(gal)	580.440
PGA_NS2(gal)	534.579
PGA_UD2(gal)	216.276
Bore_Height(m)	-224
PGA_EW1(gal)	125.169
PGA_NS1(gal)	93.941
PGA_UD1(gal)	62.495
```

## Dependencies
Just Python 2.7. 

To use this module in Python 3.0+, the `print` commands need to be rewritten.

## License
Copyright (c) 2014, Jian Shi. See LICENSE.txt file for details.
