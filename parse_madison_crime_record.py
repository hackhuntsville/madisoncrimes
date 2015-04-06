#!/usr/bin/env

import sys
import os, string, shutil, glob, time, datetime, socket, random
from geopy.geocoders import GoogleV3 

#inFileName = "160.txt"
print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)
inFileName = sys.argv[1]
inFile = open(inFileName, 'r')
lines = inFile.readlines()
inFile.close()
caseNo = []
time_of_day = []
shift = []
date_of_day = []
location = []
incident = []
latitude = []
longitude = []
sep = "%"

initial_row_id = 0
row = -1
incidents = -1

# get the geolocator.

# uncomment and edit following line to add your Google API key.
#my_google_api_key = "USE_GOOGLE_API_KEY"
my_google_api_key = "AIzaSyDu2mhJ1VTT2XcqmL8868DaG_P46m_Y5gg"

geolocator = GoogleV3(api_key=my_google_api_key)

header = 'id' + sep + 'case_no' + sep + 'time' + sep + 'shift' + sep + 'date' + sep + 'location' + sep + 'latitude' + sep + 'longitude' + sep + 'incident_type' + '\n'

# don't print new line character
print(header[:-1])

for line in lines:
    words = line.split()
    if len(words) > 0:
        #print(line)
        if line.find('Case No.:') >= 0:
            #print(words)
            row = row + 1
            caseRow = row
            incidents = -1
            for i in range(len(words)):
                #print(words[i].lower())
                if (words[i].lower() == 'no.:'):
                    caseNo.append(words[i+1])
                elif (words[i].lower() == 'time:'):
                    time_of_day.append(words[i+1] + words[i+2])
                elif (words[i].lower() == 'shift:'):
                    shift.append(words[i+1])

        elif line.find('Date Reported:') >= 0:
            #print(words)
            for i in range(len(words)):
                if (words[i].lower() == 'reported:'):
                    date_of_day.append(words[i+1] + words[i + 2] + words[i+3])
                elif (words[i].lower() == 'location:'):
                    pos = line.rfind(':')
                    endPos = len(line)
                    address = line[pos + 1:endPos - 1] + ' Madison AL'
                    
                    delay_time = random.uniform(0, 0.2)
                    time.sleep(delay_time)
                    
                    try:
                        geolocation = geolocator.geocode(address, timeout=2)
                    
                    except:
                        latitude_str = "NA_EXCEPTION"
                        longitude_str = "NA_EXCEPTION"

                    else:
                        if geolocation != None :
                            latitude_str = str(geolocation.latitude)
                            longitude_str = str(geolocation.longitude)
                        else:
                            latitude_str = "NA"
                            longitude_str = "NA"
                    
                    location.append(address)
                    latitude.append(latitude_str)
                    longitude.append(longitude_str)

                    #print(caseNo[caseRow], ' % ', location[caseRow], ' % ', latitude[caseRow], ' % ', longitude[caseRow])

        
        elif line.find('Incident:') >= 0:
            #print(words)
            pos = line.rfind(':')
            incidents = incidents + 1
            #print ('caseRow = ', caseRow, caseNo[caseRow])
            #print ('row = ', row)

            if (caseRow == (row + incidents)):
                incident.append(line[pos + 1:])
                i = caseRow
                row_id = i + initial_row_id
                out_str = str(row_id) + sep + caseNo[i] + sep + time_of_day[i] + sep + shift[i] + sep + date_of_day[i] + sep + location[i] + sep + latitude[i] + sep + longitude[i] + sep + incident[i]
                print(out_str[:-1])

            elif (caseRow < (row + incidents)):
                row = row + 1
                caseNo.append(caseNo[caseRow])
                time_of_day.append(time_of_day[caseRow])
                shift.append(shift[caseRow])
                date_of_day.append(date_of_day[caseRow])
                location.append(location[caseRow])
                latitude.append(latitude[caseRow])
                longitude.append(longitude[caseRow])
                incident.append(line[pos + 1:])

                i = row
                row_id = i + initial_row_id
                out_str = str(row_id) + sep + caseNo[i] + sep + time_of_day[i] + sep + shift[i] + sep + date_of_day[i] + sep + location[i] + sep + latitude[i] + sep + longitude[i] + sep + incident[i]
                print(out_str[:-1])
                    
#print(row)
#print(len(caseNo))
#print(caseNo)
outFileName = "madison_crime_record_with_geocode_tmp.csv"
outFile = open(outFileName, 'w')
outFile.write(header)
for i in range(len(caseNo)):
    outFile.write(str(i) + sep + caseNo[i] + sep + time_of_day[i] + sep + shift[i] + sep + date_of_day[i] + sep + location[i] + sep + latitude[i] + sep + longitude[i] + sep + incident[i])
        
outFile.close()
