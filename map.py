try: import simplejson as json
except ImportError: import json
import urllib2
from template import Template
from flask import url_for

class Listing:
    def __init__(self, listing_json):
        self.price = listing_json['price']
        self.rooms = listing_json['bedroom_number']
        if listing_json['bedroom_number'] =='' or '0' or ' ':
            self.rooms = '1'
        else:
            self.rooms = listing_json['bedroom_number']
        self.title = listing_json['title']
        self.location = {'lat':listing_json['latitude'], 'lng' : listing_json['longitude']}
        self.img = listing_json['img_url']
        self.keywords = listing_json['keywords']
        self.source = listing_json['datasource_name']
        self.bathrooms = listing_json['bathroom_number']
        self.perroom = self.price/int(self.rooms) 

def geocode(addr):
    """ Fetch geocoded location. 
    INPUT: 
        A string of an address. Any address. 
    RETURNS: 
        Location as a dictionary 'lat' and 'lng' as keys
    Currently we are using the google maps geocoding api located at  
    http://code.google.com/apis/maps/documentation/geocoding/ 
    It only allows 2500 requests a day.
    Perhaps, given this will mainly be used by students, we catch requests to google that have previously
    been requested - use redis or save to txt file with python?"""
    url ="http://maps.googleapis.com/maps/api/geocode/json?address={0}&sensor=false".format(addr)
    fetched_json = urllib2.urlopen(url).read()
    pythonified_json = json.loads(fetched_json)
    location = pythonified_json['results'][0]['geometry']['location'] 
    return location

def fetchResults(location):
    """Fetches property listings from the Nestoria API. 
    INPUT: 
        A dictionary specifying a location. 'lat' and 'lng' as keys
    RETURNS: 
        A python datastructure based on the rules the json library uses."""
    url = "http://api.nestoria.co.uk/api?action=search_listings&encoding=json&centre_point={0},{1},5km&listing_type=rent&number_of_results=50&sort=newest".format(location['lat'],location['lng'])
    fetched_json = urllib2.urlopen(url).read()
    pythonified_json = json.loads(fetched_json)
    return pythonified_json

def listListings(location):
    results = fetchResults(geocode(location))['response']['listings']
    listings = []
    for listing in results:
        listings.append(Listing(listing))
    return listings

def generateMap(location):
    ''' Pull the template, replace some variables.'''
    page = Template("template.html")
    coord = geocode(location) #grab the centrepoint from the Google Geocoding API
    page.replaceVariable('$location', "{0},{1}".format(coord['lat'],coord['lng']))
    index = page.findJS() 
    page.data.pop(index)
    js = createJavascript(location,index)
    page.data.insert(index,js)
    page.outputDoc("output.html")
    page_out = open("output.html", 'r')
    return page_out.read()

def createJavascript(location, index):
    js = """ \t var markerLocation = new L.LatLng({1}); \n var marker{0} = new L.Marker(markerLocation); \n map.addLayer(marker{0}); \n  marker{0}.bindPopup("<b>{2}</b><br />{3}<a href = '{4}'>{5}</a>"); \n"""
    results = listListings(location)
    marker_entries = []
    for num in range(len(results)):
        marker_entries.append(js.format(num,results[num].location['lat']+','+results[num].location['lng'],results[num].title,results[num].perroom,results[num].img, results[num].keywords))
    return marker_entries


