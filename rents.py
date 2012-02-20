from flask import Flask
import main_page
import location

rents = flask(__name__)

@rents.route("/")
def main_page():
    return main_page

@rents.route("/<location>")
def location_view(location):
    pass
