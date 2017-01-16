# -*- coding: utf-8 -*-
"""
Created on Sat May 24 15:26:24 2014

Copyright (c) 2012-2014, Jian Shi
"""

def convert_single_event(parent_folder,event_name,station_type):
    '''
    Convert from Kyoshin ASCII format to 2-column format (for a single event).
    [Note] PARENT_FOLDER must not include EVENT_NAME.
    '''

    import os

    folder = parent_folder + os.sep + event_name

    if station_type == 'kik':
        nr = 6
        channel = ['EW1','EW2','NS1','NS2','UD1','UD2']
        for i in range(nr):
            f = open(folder + os.sep + event_name + '.' + channel[i],'r') # open file to read
            data = f.readlines()

            if i == 0: # only need to be read once
                ## Line 0: Origin time of event
                origin_date_and_time = data[0][18:-1] # start from the 18th entry
                [origin_date,origin_time] = origin_date_and_time.split(' ')

                ## Line 1: Latitute
                latitute = data[1][18:-1] # data type: string

                ## Line 2: Longtitute
                longitute = data[2][18:-1]

                ## Line 3: Depth in km
                depth_in_km = data[3][18:-1]

                ## Line 4: Magnitute
                magnitute = data[4][18:-1]

                ## Line 5: Station code
                station_code = data[5][18:-1]

                ## Line 6: Station latitute
                station_lat = data[6][18:-1]

                ## Line 7: Station longitute
                station_lon = data[7][18:-1]

            ## Line 8: Station height (in m)
            if i == 0: # EW1: borehole
                height_borehole = data[8][18:-1]
            if i == 1: # EW2: surface
                height_surface = data[8][18:-1]

            if i == 0: # only need to be read once
                ## Line 9: Record date and time
                record_date_and_time = data[9][18:-1]
                [record_date,record_time] = record_date_and_time.split(' ')

                ## Line 10: Sampling frequency (Hz)
                sampling_freq = data[10][18:-1] # a string like "200Hz"
                for j in range(len(sampling_freq)):
                    if sampling_freq[j] == 'H':
                        sampling_freq = sampling_freq[:j]
                        break

                ## Line 11: Duration time (sec)
                duration_time = data[11][18:-1]

            ## Line 12: Direction -- obmitted

            ## Line 13: Scale factor (NOTE: different for different channels)
            scale_factor_str = data[13][18:-1] # example: 2940(gal)/6170270
            scale_factor_str2 = scale_factor_str.split('(gal)/')
            numerator = float(scale_factor_str2[0])
            denominator = float(scale_factor_str2[1])
            scale_factor = numerator / denominator # float

            ## Line 14: Maximum acceleration in gal
            if i == 0: PGA_EW1 = data[14][18:-1]
            if i == 1: PGA_EW2 = data[14][18:-1]
            if i == 2: PGA_NS1 = data[14][18:-1]
            if i == 3: PGA_NS2 = data[14][18:-1]
            if i == 4: PGA_UD1 = data[14][18:-1]
            if i == 5: PGA_UD2 = data[14][18:-1]

            ## Line 15: Last correction date and time
            if i == 0: # only need to be read once
                last_corr_date_and_time = data[15][18:-1]
                [last_corr_date,last_corr_time] = last_corr_date_and_time.split(' ')

            ## Line 16: "Memo." -- obmitted

            ## From Line 17: Start raw data
            accel_list = [] # preallocation of acceleration list
            for row_idx in range(17,len(data)):
                current_line = data[row_idx][:-1]
                current_line_list = current_line.split() # using split() without argument: split on white spaces
                for kk in range(len(current_line_list)):
                    accel = current_line_list[kk] # string
                    accel = float(accel) # str --> float
                    accel = accel * scale_factor
                    accel = str(accel) # convert back to string
                    accel_list.append(accel)

            # # # # File reading finished. Start writing acceleration to file # # #
            ## Construct time array
            dt = 1.0 / float(sampling_freq)
            time = [x*dt for x in range(1,len(accel_list)+1)] # time array

            ## Length check
            if len(accel_list) != len(time):
                print 'Two lengths not consistent. The script could terminate...'

            ## Export to file
            out_filename = folder + os.sep + event_name + '.' + channel[i] + '.txt'
            f_out = open(out_filename,'w') # open a file for writing
            for k in range(len(time)):
                f_out.write(str(time[k]))
                f_out.write('\t')
                f_out.write(str(accel_list[k]))
                f_out.write('\n')
            f_out.close()
            if i == 0:
                print event_name, channel[i]
            else:
                print '                ', channel[i]
            del f_out

        ## Writing basic info to file
        info_filename = folder + os.sep + event_name + '.basic_info.txt'
        f_info = open(info_filename,'w')
        f_info.write('Station_Name\t' + station_code + '\n')
        f_info.write('Station_Lat\t' + station_lat + '\n')
        f_info.write('Station_Lon\t' + station_lon + '\n')
        f_info.write('Origin_Date\t' + origin_date + '\n')
        f_info.write('Origin_Time\t' + origin_time + '\n')
        f_info.write('Rec_Start_Date\t' + record_date + '\n')
        f_info.write('Rec_Start_Time\t' + record_time + '\n')
        f_info.write('Duration_Time(s)\t' + duration_time + '\n')
        f_info.write('Last_Corr_Date\t' + last_corr_date + '\n')
        f_info.write('Last_Corr_Time\t' + last_corr_time + '\n')
        f_info.write('EQ_Lat\t' + latitute + '\n')
        f_info.write('EQ_Lon\t' + longitute + '\n')
        f_info.write('EQ_Mag\t' + magnitute + '\n')
        f_info.write('EQ_Depth(km)\t' + depth_in_km + '\n')
        f_info.write('Samp_Freq(Hz)\t' + sampling_freq + '\n')
        f_info.write('Surf_Height(m)\t' + height_surface + '\n')
        f_info.write('PGA_EW2(gal)\t' + PGA_EW2 + '\n')
        f_info.write('PGA_NS2(gal)\t' + PGA_NS2 + '\n')
        f_info.write('PGA_UD2(gal)\t' + PGA_UD2 + '\n')
        f_info.write('Bore_Height(m)\t' + height_borehole + '\n')
        f_info.write('PGA_EW1(gal)\t' + PGA_EW1 + '\n')
        f_info.write('PGA_NS1(gal)\t' + PGA_NS1 + '\n')
        f_info.write('PGA_UD1(gal)\t' + PGA_UD1 + '\n')
        f_info.close()
        print '                ', 'Basic Info', '-- Done.'

    if station_type == 'k':
        nr = 3
        channel = ['EW','NS','UD']
        for i in range(nr):
            f = open(folder + os.sep + event_name + '.' + channel[i],'r') # open file to read
            data = f.readlines()

            if i == 0: # only need to be read once
                ## Line 0: Origin time of event
                origin_date_and_time = data[0][18:-1] # start from the 18th entry
                [origin_date,origin_time] = origin_date_and_time.split(' ')

                ## Line 1: Latitute
                latitute = data[1][18:-1] # data type: string

                ## Line 2: Longtitute
                longitute = data[2][18:-1]

                ## Line 3: Depth in km
                depth_in_km = data[3][18:-1]

                ## Line 4: Magnitute
                magnitute = data[4][18:-1]

                ## Line 5: Station code
                station_code = data[5][18:-1]

                ## Line 6: Station latitute
                station_lat = data[6][18:-1]

                ## Line 7: Station longitute
                station_lon = data[7][18:-1]

                ## Line 8: Station height (in m)
                station_height = data[8][18:-1]

                ## Line 9: Record date and time
                record_date_and_time = data[9][18:-1]
                [record_date,record_time] = record_date_and_time.split(' ')

                ## Line 10: Sampling frequency (Hz)
                sampling_freq = data[10][18:-1] # a string like "200Hz"
                for j in range(len(sampling_freq)):
                    if sampling_freq[j] == 'H':
                        sampling_freq = sampling_freq[:j]
                        break

                ## Line 11: Duration time (sec)
                duration_time = data[11][18:-1]

            ## Line 12: Direction -- obmitted

            ## Line 13: Scale factor (NOTE: different for different channels)
            scale_factor_str = data[13][18:-1] # example: 2940(gal)/6170270
            scale_factor_str2 = scale_factor_str.split('(gal)/')
            numerator = float(scale_factor_str2[0])
            denominator = float(scale_factor_str2[1])
            scale_factor = numerator / denominator # float

            ## Line 14: Maximum acceleration in gal
            if i == 0: PGA_EW = data[14][18:-1]
            if i == 1: PGA_NS = data[14][18:-1]
            if i == 2: PGA_UD = data[14][18:-1]

            ## Line 15: Last correction date and time
            if i == 0: # only need to be read once
                last_corr_date_and_time = data[15][18:-1]
                [last_corr_date,last_corr_time] = last_corr_date_and_time.split(' ')

            ## Line 16: "Memo." -- obmitted

            ## From Line 17: Start raw data
            accel_list = [] # preallocation of acceleration list
            for row_idx in range(17,len(data)):
                current_line = data[row_idx][:-1]
                current_line_list = current_line.split() # using split() without argument: split on white spaces
                for kk in range(len(current_line_list)):
                    accel = current_line_list[kk] # string
                    accel = float(accel) # str --> float
                    accel = accel * scale_factor
                    accel = str(accel) # convert back to string
                    accel_list.append(accel)

            # # # # File reading finished. Start writing acceleration to file # # #
            ## Construct time array
            dt = 1.0 / float(sampling_freq)
            time = [x*dt for x in range(1,len(accel_list)+1)] # time array

            ## Length check
            if len(accel_list) != len(time):
                print 'Two lengths not consistent. The script could terminate...'

            ## Export to file
            out_filename = folder + os.sep + event_name + '.' + channel[i] + '.txt'
            f_out = open(out_filename,'w') # open a file for writing
            for k in range(len(time)):
                f_out.write(str(time[k]))
                f_out.write('\t')
                f_out.write(str(accel_list[k]))
                f_out.write('\n')
            f_out.close()
            if i == 0:
                print event_name, channel[i]
            else:
                print '                ', channel[i]
            del f_out

        ## Writing basic info to file
        info_filename = folder + os.sep + event_name + '.basic_info.txt'
        f_info = open(info_filename,'w')
        f_info.write('Station_Name\t' + station_code + '\n')
        f_info.write('Station_Lat\t' + station_lat + '\n')
        f_info.write('Station_Lon\t' + station_lon + '\n')
        f_info.write('Origin_Date\t' + origin_date + '\n')
        f_info.write('Origin_Time\t' + origin_time + '\n')
        f_info.write('Rec_Start_Date\t' + record_date + '\n')
        f_info.write('Rec_Start_Time\t' + record_time + '\n')
        f_info.write('Duration_Time(s)\t' + duration_time + '\n')
        f_info.write('Last_Corr_Date\t' + last_corr_date + '\n')
        f_info.write('Last_Corr_Time\t' + last_corr_time + '\n')
        f_info.write('EQ_Lat\t' + latitute + '\n')
        f_info.write('EQ_Lon\t' + longitute + '\n')
        f_info.write('EQ_Mag\t' + magnitute + '\n')
        f_info.write('EQ_Depth(km)\t' + depth_in_km + '\n')
        f_info.write('Samp_Freq(Hz)\t' + sampling_freq + '\n')
        f_info.write('Sta_Height(m)\t' + station_height + '\n')
        f_info.write('PGA_EW(gal)\t' + PGA_EW + '\n')
        f_info.write('PGA_NS(gal)\t' + PGA_NS + '\n')
        f_info.write('PGA_UD(gal)\t' + PGA_UD + '\n')
        f_info.close()
        print '                ', 'Basic Info', '-- Done.'

def convert_multiple_events(parent_folder):
    '''
    Convert from Kyoshin ASCII format to 2-column format.

    PARENT_FOLDER contains many subfolders that have Kik-Net or K-Net raw ASCII
    files. The program only looks at subfolders whose folder name's length has
    sixteen characters, i.e., IWTH041103111446.

    Station type (i.e., Kik or K) is determined automatically by counting the
    number of files within the subfolder. If 8 files, Kik; if 5 files, K.
    '''

    import os
   
    folder_list = [d for d in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder,d))]
    for i in range(len(folder_list)):
        folder_name = folder_list[i]
        if len(folder_name) == 16:
            file_list = os.listdir(parent_folder + os.sep + folder_name)
            if len(file_list) == 8:
                station_type = 'kik'
                convert_single_event(parent_folder,folder_name,station_type)
            elif len(file_list) == 5:
                station_type = 'k'
                convert_single_event(parent_folder,folder_name,station_type)
            else:
                print folder_name, ' -- skipped.'

