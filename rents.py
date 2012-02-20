from flask import Flask
import urllib2
try: import simplejson as json
except ImportError: import json

rents = Flask(__name__)

@rents.route("/")
def main_page():
    pass

@rents.route("/<location>")
def location_view(location):
    pass

def geocode(addr):
    """ Fetch geocoded location. Currently we are using the google maps geocoding api located at  http://code.google.com/apis/maps/documentation/geocoding/ It only allows 2500 requests a day. An option to get around this later is to embed this request client-side or perhaps to explore the use of OpenStreetMap?"""
    url ="http://maps.googleapis.com/maps/api/geocode/json?address={0}&sensor=false".format(addr)
    fetched_json = urllib2.urlopen(url).read()
    pythonified_json = json.loads(fetched_json)
    location = pythonified_json['results'][0]['geometry']['location'] #stored as dict. To get lat go location['lat']
    return location

geocode("Glasgow%20University") #note '%20' only needs to be in for testing purposes since the browser will automatically change a space into '%20' when sending the request to the handler. 
