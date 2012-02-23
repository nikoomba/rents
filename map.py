try: import simplejson as json
except ImportError: import json
import urllib2
from template import Template
from flask import url_for

def geocode(addr):
    """ Fetch geocoded location. Currently we are using the google maps geocoding api located at  
    http://code.google.com/apis/maps/documentation/geocoding/ It only allows 2500 requests a day.
    An option to get around this later is to embed this request client-side or perhaps to explore
    the use of OpenStreetMap?"""
    url ="http://maps.googleapis.com/maps/api/geocode/json?address={0}&sensor=false".format(addr)
    fetched_json = urllib2.urlopen(url).read()
    pythonified_json = json.loads(fetched_json)
    location = pythonified_json['results'][0]['geometry']['location'] #stored as dict. To get lat go location['lat']
    return location

def fetchResults(location):
    """Fetches property listings from the Nestoria API. Takes as input a dictionary specifying a location in lat and lng"""
    url = "http://api.nestoria.co.uk/api?action=search_listings&encoding=json&centre_point={0},{1},5km&listing_type=rent&number_of_results=50&sort=newest".format(location['lat'],location['lng'])
    fetched_json = urllib2.urlopen(url).read()
    pythonified_json = json.loads(fetched_json)
    return pythonified_json

class Listings:
    """ ISSUE *This could just be a list (silly me)
              *some other issue ."""

    def __init__(self, location):
        x = fetchResults(geocode(location))['response']['listings']
        lyst = []
        for listing in x:
            lyst.append(Listing(listing))
        self.listings = lyst
        self.number = len(lyst)
    def printListings(self):
        for listing in self.listings:
            print listing.title
    
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

'''These two functions work, but are a mess'''
def generateMap(location):
    ''' Pull the template, replace some variables.
        To ADD: 
              *check all variables are replaced.
              
    '''
    x = Template("template.html")
    geocode = geocode(location) #grab the centrepoint from the Google Geocoding API
    x.replaceVariable('$location', "{0},{1}".format(geocode['lat'],geocode['lng']))
    index = x.findJS() 
    x.data.pop(index)
    js = createJavascript(location,index)
    x.data.insert(index,js)
    x.outputDoc("output.html")
    page = open("output.html", 'r')
    return page.read()

def createJavascript(location, index):
    js = """ \t var markerLocation = new L.LatLng({1}); \n var marker{0} = new L.Marker(markerLocation); \n map.addLayer(marker{0}); \n  marker{0}.bindPopup("<b>{2}</b><br />{3}<a href = '{4}'>{5}</a>"); \n"""
    results = Listings(location)
    marker_entries = []
    for num in range(len(results.listings)):
        marker_entries.append(js.format(num,results.listings[num].location['lat']+','+results.listings[num].location['lng'],results.listings[num].title,results.listings[num].perroom,results.listings[num].img, results.listings[num].location))
    return marker_entries

""" ISSUE test 3 .""""
#print generateMap("Oxford%University")
#print geocode("Oxford%20University")
