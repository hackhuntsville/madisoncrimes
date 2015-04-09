from app import db
from geoalchemy2 import Geometry

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    geom = db.Column(Geometry('POINT'))

    def __repr__(self):
        return '<Location %r>' % (self.name)


class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)

    def __repr__(self):
        return '<Incident %r>' % (self.name)


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mad_id = db.Column(db.String)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    location = db.relationship("Location")
    incident_id = db.Column(db.Integer, db.ForeignKey('incident.id'))
    incident = db.relationship("Incident")
    shift = db.Column(db.Integer)
    date = db.Column(db.DateTime)

    def __repr__(self):
        return '<Record %r>' % (self.mad_id)
