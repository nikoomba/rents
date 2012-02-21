from flask import Flask
from map import geocode

app = Flask(__name__)

@app.route("/")
def main_page():
    page = open("main.html", 'r')
    return page.read()

@app.route("/<loc>")
def location_view(loc):
    loc = loc.replace(' ','_')
    """------- testing the geocoding function
    x = geocode(loc)
    (lat,lng)=(x['lat'],x['lng'])
    return "Lat: {0}, Long: {1}".format(lat,lng)
    ---------- test"""

"""Run Flask if this file is executed by python. Useful to comment this out for testing in the commandline, or else uncomment the 'app.debug=True' line"""
if __name__ == '__main__':
    app.debug = True
    app.run()

