#!/usr/bin/env

import sys
import os, string, shutil, glob, time, datetime, socket, random
import csv, json

csvFileName = sys
print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)
csvFileName = sys.argv[1]


csvfile = open(csvFileName, 'r')
jsonfile = open(csvFileName.replace('.csv','.json'), 'w')

jsonfile.write('{"' + 'madison_crime_data' + '": [\n')       # write json parent of data list
fieldnames = csvfile.readline().replace('\n','').split('%')                         # get fieldnames from first line of csv
num_lines = sum(1 for line in open(csvFileName)) - 1                                   # count total lines in csv minus header row

reader = csv.DictReader(csvfile, fieldnames, delimiter='%')                                        
i = 0
for row in reader:
  i += 1
  json.dump(row, jsonfile)
  if i < num_lines:
    jsonfile.write(',')
  jsonfile.write('\n')
jsonfile.write(']}')
