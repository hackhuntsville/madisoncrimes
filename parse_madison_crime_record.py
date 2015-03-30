#!/usr/bin/env

import sys
import os, string, shutil, glob, time, datetime, socket

#inFileName = "160.txt"
print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)
inFileName = sys.argv[1]
inFile = open(inFileName, 'r')
lines = inFile.readlines()
inFile.close()
caseNo = []
time = []
shift = []
date = []
location = []
incident = []

row = -1
incidents = -1

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
                    time.append(words[i+1] + words[i+2])
                elif (words[i].lower() == 'shift:'):
                    shift.append(words[i+1])

        elif line.find('Date Reported:') >= 0:
            #print(words)
            for i in range(len(words)):
                if (words[i].lower() == 'reported:'):
                    date.append(words[i+1] + words[i + 2] + words[i+3])
                elif (words[i].lower() == 'location:'):
                    pos = line.rfind(':')
                    endPos = len(line)
                    location.append(line[pos + 1:endPos - 1])
        
        elif line.find('Incident:') >= 0:
            #print(words)
            pos = line.rfind(':')
            incidents = incidents + 1
            #print ('caseRow = ', caseRow, caseNo[caseRow])
            #print ('row = ', row)
            if (caseRow == (row + incidents)):
                incident.append(line[pos + 1:])
            elif (caseRow < (row + incidents)):
                row = row + 1
                caseNo.append(caseNo[caseRow])
                time.append(time[caseRow])
                shift.append(shift[caseRow])
                date.append(shift[caseRow])
                location.append(location[caseRow])
                incident.append(line[pos + 1:])
                    
#print(row)
#print(len(caseNo))
#print(caseNo)
outFileName = "madison_crime_record.csv"
outFile = open(outFileName, 'w')
outFile.write("id,case_no,time,shift,date,location,type"+'\n')

for i in range(len(caseNo)):
    outFile.write(str(i) + ',' + caseNo[i] + ',' + time[i] + ',' + shift[i] + ',' + date[i] + ',' + location[i] + ',' + incident[i])
        
outFile.close()
