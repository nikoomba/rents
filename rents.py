from flask import Flask
import urllib2
try: import simplejson as json
except ImportError: import json

app = Flask(__name__)

@app.route("/")
def main_page():
    return "Hello World! Change me later!"

@app.route("/<loc>")
def location_view(loc):
    x = geocode(loc)
    (lat,lng)=(x['lat'],x['lng'])
    return "Lat: {0}, Long: {1}".format(lat,lng)

def geocode(addr):
    """ Fetch geocoded location. Currently we are using the google maps geocoding api located at  http://code.google.com/apis/maps/documentation/geocoding/ It only allows 2500 requests a day. An option to get around this later is to embed this request client-side or perhaps to explore the use of OpenStreetMap?"""
    url ="http://maps.googleapis.com/maps/api/geocode/json?address={0}&sensor=false".format(addr)
    fetched_json = urllib2.urlopen(url).read()
    pythonified_json = json.loads(fetched_json)
    location = pythonified_json['results'][0]['geometry']['location'] #stored as dict. To get lat go location['lat']
    return location

#geocode("Glasgow") #note '%20' only needs to be in for testing purposes since the browser will automatically change a space into '%20' when sending the request to the handler. 

"""Run Flask if this file is executed by python. Useful to comment this out for testing in the commandline, or else uncomment the 'app.debug=True' line"""

if __name__ == '__main__':
    app.debug = True
    app.run()

