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
    """This could just be a list (silly me)"""
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
    

def generateMap(location):
    x = Template("template.html")
    geocoded = geocode(location)
    x.replaceVariable('$location', "{0},{1}".format(geocoded['lat'],geocoded['lng']))
    x.outputDoc("output.html")
    page = open("output.html", 'r')
    return page.read()

def createJavascript(location):
    js = """var marker{0} = new L.Marker({1}); map.addLayer(marker{0}); marker{0}.bindPopup("<b>{2}</b><br />{3}<a href = '{4}'>{5}</a>")"""
    results = Listings(location)
    marker_entries = []
    for num in range(len(results.listings)):
        marker_entries.append(js.format(num,results.listings[num].location['lat']+','+results.listings[num].location['lng'],results.listings[num].title,results.listings[num].perroom,results.listings[num].img, results.listings[num].location))
    return marker_entries

print createJavascript("London%20School%20of%20Economics")
    

js = """var marker{0} = new L.Marker({1});
map.addLayer(marker{0});
marker{0}.bindPopup("<b>{2}</b><br />{3}<a href = '{4}'>link</a>")"""

""" 0 = marker number
1 = marker location (lat,lng)
2 = title
3 = summary
4 = link
"""

print js.format('1337','lat,lng','a very nice title','some lousy description','http://awesomeness.hai')

#print generateMap("Oxford%University")
#print geocode("Oxford%20University")
