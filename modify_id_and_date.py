#!/usr/bin/env

import sys
import os, string, shutil, glob, time, datetime, socket, random, csv
from geopy.geocoders import GoogleV3 

#inFileName = "160.txt"
print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

inFileName = sys.argv[1]
initial_row_id = int(sys.argv[2])
outFileName = sys.argv[3]

inFile = open(inFileName, 'rt')
caseNo = []
time_of_day = []
shift = []
date_of_day = []
location = []
incident = []
latitude = []
longitude = []
sep = "%"

#initial_row_id = 0
i = -1
incidents = -1

try: 
    reader = csv.DictReader(inFile, delimiter = '%')
    for row in reader:
        i = i + 1
        caseNo.append(row[' case_no '].strip(" "))
        time_of_day.append(row[' time '].strip(" "))
        shift.append(row[' shift '].strip(" "))
        if row[' date '] == row[' shift ']:
            date_of_day.append(date_of_day[i - 1])
        else:
            date_of_day.append(row[' date '].strip(" "))
        location.append(row[' location '].strip(" "))
        latitude.append(row[' latitude '].strip(" "))
        longitude.append(row[' longitude '].strip(" "))
        incident.append(row[' incident_type'].strip(" "))
        
finally:
    inFile.close()


header = 'id' + sep + 'case_no' + sep + 'time' + sep + 'shift' + sep + 'date' + sep + 'location' + sep + 'latitude' + sep + 'longitude' + sep + 'incident_type' + '\n'

#outFileName = "madison_crime_record_with_geocode_0_1615.csv"
outFile = open(outFileName, 'w')
outFile.write(header)
for i in range(len(caseNo)):
    row_id = i + initial_row_id
    outFile.write(str(row_id) + sep + caseNo[i] + sep + time_of_day[i] + sep + shift[i] + sep + date_of_day[i] + sep + location[i] + sep + latitude[i] + sep + longitude[i] + sep + incident[i]+'\n')
        
outFile.close()
