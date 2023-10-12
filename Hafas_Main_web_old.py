import datetime
from typing import List
from flask import Flask, render_template, request, make_response
import json
import requests

app = Flask(__name__)

def get_departure_info(station_name):
    url = f"https://dbf.finalrewind.org/{station_name}.json?version=3"
    response = requests.get(url)
    if response.status_code == 200:
        departures_data = response.json().get("departures", [])
        departures = [station_board_leg_to_dict(leg) for leg in departures_data]
        return departures
    else:
        return []

def station_board_leg_to_dict(leg):
    return {
        "name": leg["train"],
        "direction": leg["destination"],
        "dateTime": leg["scheduledDeparture"],
        "delay": leg["delayDeparture"],
        "platform": leg["scheduledPlatform"],
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    departures = []
    station_name = ""

    # Get the station name from the form input
    if request.method == 'POST':
        station_name = request.form['station_name']
        departures = get_departure_info(station_name)
    
    return render_template('index.html', departures=departures, station_name=station_name)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)
