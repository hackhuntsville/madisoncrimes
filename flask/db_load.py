#!/usr/bin/env python

from app import db, models

import csv
import time

fname = '../madison_crime_record_with_geocode.csv'

csvfile = open(fname, 'r')
fieldnames = csvfile.readline().replace('\n','').split('%')

reader = csv.DictReader(csvfile, fieldnames, delimiter='%')

models.Record.query.delete()
models.Location.query.delete()
models.Incident.query.delete()
db.reflect()
db.create_all()

locations = {}
incidents = {}

def sanitize_address(l):
    l = l.replace('Madison Madison Madison ', 'Madison ')
    l = l.replace('Madison Madison ', 'Madison ')
    l = l.replace('Ln ', 'Lane ')
    l = l.replace('Dr ', 'Drive ')
    l = l.replace('St ', 'Street ')
    l = l.replace('Pl ', 'Place ')
    l = l.replace('Rd ', 'Road ')
    l = l.replace('Ct ', 'Court ')
    return l

def sanitize_incident(l):
    return l

for row in reader:
    print row
    location_name = sanitize_address(row['location'])
    if not locations.has_key(location_name):
        locations[location_name] = models.Location(name=location_name,
                geom='POINT(%s %s)' % (row['longitude'], row['latitude']))

    incident_name = sanitize_incident(row['incident_type'])
    if not incidents.has_key(incident_name):
        incidents[incident_name] = models.Incident(name=incident_name)

    shift_dict = { 'I': 1, 'II': 2, 'III': 3}

    record = models.Record()
    record.mad_id = row['case_no']
    record.location = locations[location_name]
    record.incident = incidents[incident_name]
    #record.shift = shift_dict[row['shift']] 

    date = time.strptime(row['date'], '%B%d,%Y')
    time = time.strptime(row['time'], '%I:%M%p')

    print (date, time)


    db.session.add(record)
    db.session.commit()
    break
