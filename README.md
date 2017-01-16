# K-net/KiK-net ASCII conversion
#### Converts K-NET or KiK-net raw ASCII data files into usable ASCII waveforms

## Description
The original ASCII data format from the K-NET and KiK-net database (http://www.kyoshin.bosai.go.jp/) is very cumbersome to use. This module can convert the original data format into ready-to-use 2-column waveform format (i.e., 1st column = time, 2nd column = ground acceleration).

## How to use this module

1. Download seismograms from K/Kik-net website to the hard drive, and arrange the folders in the following fashion:
  ```
    [FKSH14] 
      | 
      | 
      | 
  ```

Put `kyoshin_bosai.py` into your Python search path



, then,

```Python
import kyoshin_bosai
kyoshin_bosai.convert_single_event(parent_folder,event_name,station_type)
```
