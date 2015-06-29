#!/usr/bin/env python

import os
import subprocess
import sys
import re

import pandas as pd

from lxml import html
import requests
import urllib2

MADISON_URL = 'https://www.madisonal.gov/Archive.aspx'

def list_all_urls():
    '''
    On Madison Incident Report archive, list all of the files available
    '''
    payload = {'AMID':'67','Type':'','ADID':''}
    page = requests.get(MADISON_URL, params=payload)
    tree = html.fromstring(page.text)
    urls = tree.xpath('//span[@class="archive"]/a')

    ret = []

    for url in urls:
        url_s = url.attrib['href']
        url_s = url_s.split('=')
        if len(url_s) <  2:
            continue
        ret.append(url_s[1])
    return ret

def files_already_downloaded():
    return os.listdir('pdfs')

def download_pdf(file):
    payload = {'ADID': file}
    page = requests.get(MADISON_URL, params=payload)
    f = open( "pdfs/" + file, 'wb' )
    f.write( page.content )
    f.close()

def convert_to_text(file):
    return subprocess.check_output(["pdftotext", "-nopgbrk", "-layout",
                ('pdfs/' + file), '-']).split('\n')

def clean_lines(lines):
    lines_new = []
    for line in lines:
        if line == '\n':
            continue

        s = ['Madison Police Department',
             'Incident Report',
             'indicent report']

        find = [line.find(x) >= 0 for x in s]
        line = line.strip('\n')
        line = line.strip('\x0c')

        if (line.find('( ') >= 0 and
           line.find(' )') >= 0 and
           (line.find('To') >= 0 or line.find('to') >= 0)):
           continue

        if any(find):
            continue

        s = [ 'Case No.:',
              'Date Reported:',
              'Time:',
              'Shift:',
              'Location:',
              'Incident:']

        find = [line.find(x) >=0 for x in s]

        if not any(find) and len(lines_new) >= 1:
            lines_new[-1] = lines_new[-1] + " " + line
        else:
            line = line.strip('\n')
            lines_new.append(line)

    return lines_new

def extract_records(lines, file=None):
    records = []
    record = None

    cno_lines = {}
    time_lines = {}
    shift_lines = {}
    date_lines = {}
    loc_lines = {}
    inc_lines = {}
    line_idx = [ cno_lines, time_lines, shift_lines, date_lines, loc_lines, inc_lines]

    case_str = "Case No.: "
    time_str = "Time: "
    shift_str = "Shift: "
    date_str = "Date Reported: "
    loc_str = "Location: "
    inc_str = "Incident: "
    strings = [ case_str, time_str, shift_str, date_str, loc_str, inc_str ]

    # Sort each line into it's own dict by line type
    for ii, line in enumerate(lines):
        for (_str, _idx) in zip(strings, line_idx):
            if line.find(_str) >= 0:
                _idx[ii] = line[line.find(_str) + len(_str):].strip()

    cno_keys = sorted(cno_lines.keys())
    cno_keys_s = cno_keys[1:] + [1e6]

    for key, key_plus in zip(cno_keys, cno_keys_s):
        time = [v for (k,v) in time_lines.iteritems() if
                    k > key and k < key_plus]
        date = [v for (k,v) in date_lines.iteritems() if
                    k > key and k < key_plus]
        shift = [v for (k,v) in shift_lines.iteritems() if
                    k > key and k < key_plus]
        loc = [v for (k,v) in loc_lines.iteritems() if
                    k > key and k < key_plus]
        incs = [v for (k,v) in inc_lines.iteritems() if
                    k > key and k < key_plus]

        for inc in incs:
            record = {}
            if file:
                record['File'] = file
            record['Case'] = cno_lines[key]
            record['Time'] = time[0]
            record['Date'] = date[0]
            #record['DateTime'] = pd.to_datetime(
            record['Shift'] = shift[0]
            record['Address'] = loc[0]
            record['Incident'] = inc
            record['NumInc'] = len(incs)
            records.append(record)

    return records

def clean_lines_layout(lines):
    new_lines = []
    for line in lines:
        if line.find('Time:') > 0:
            new_lines.append(line[0:line.find('Time:')])
            line = line[line.find('Time:'):]
        if line.find('Shift:') > 0:
            new_lines.append(line[0:line.find('Shift:')])
            line = line[line.find('Shift:'):]
        if line.find('Location:') > 0:
            new_lines.append(line[0:line.find('Location:')])
            line = line[line.find('Location:'):]
        new_lines.append(line)
    new_lines = [l.strip() for l in new_lines if len(l)]
    return new_lines

if __name__ == '__main__':
    all_files = set(list_all_urls())
    old_files = set(files_already_downloaded())
    new_files = all_files.difference(old_files)

    for file in new_files:
        print "Downloading: " + str(file)
        download_pdf(file)

    all_records = []
    for file in old_files:
        lines = convert_to_text(file)
        lines = clean_lines_layout(lines)
        records = extract_records(lines, file)
        all_records.extend(records)
    print pd.DataFrame(all_records)

