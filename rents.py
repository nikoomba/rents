from flask import Flask
from map import *

app = Flask(__name__)


@app.route("/")
def main_page():
    page = open("main.html", 'r')
    return page.read()

@app.route("/<loc>")
def location_view(loc):
    loc = loc.replace(' ','_')
    return generateMap(loc)

@app.route("/about.html")
def get_about():
    return open('about.html', 'r').read()

if __name__ == '__main__':
    app.debug = True
    app.run()

