from flask import Flask
from map import geocode

app = Flask(__name__)

@app.route("/")
def main_page():
    return "Hello World! Change me later! This mainpage will just be a simple sort of search box"

@app.route("/<loc>")
def location_view(loc):
    loc = loc.replace(' ','_')
    x = geocode(loc)
    (lat,lng)=(x['lat'],x['lng'])
    return "Lat: {0}, Long: {1}".format(lat,lng)

"""Run Flask if this file is executed by python. Useful to comment this out for testing in the commandline, or else uncomment the 'app.debug=True' line"""

if __name__ == '__main__':
    app.debug = True
    app.run()

