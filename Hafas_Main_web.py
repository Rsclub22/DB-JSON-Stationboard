import datetime
from typing import List
from flask import Flask, render_template, request, make_response
import json

# Part 1: Importieren der erforderlichen Module und Erstellen des Hafas-Clients
from pyhafas import HafasClient
from pyhafas.profile import DBProfile
from pyhafas.types.fptf import Leg

app = Flask(__name__)
client = HafasClient(DBProfile())

# Part 2: Suchen Sie nach der Haltestelle basierend auf der Benutzereingabe
def get_departures(station_name):
    locations = client.locations(station_name)
    if locations:
        best_found_location = locations[0]
        return best_found_location
    else:
        return None

def station_board_leg_to_dict(leg):
  delay_in_seconds = 0
  if leg.delay is not None:
      delay_in_seconds = leg.delay.total_seconds() // 60
  return {
    "name": leg.name,
    "direction": leg.direction,
    "dateTime": leg.dateTime.strftime("%Y-%m-%d %H:%M:%S"),
    "delay": delay_in_seconds,
    "platform": leg.platform,
  }


# Part 3: Rufen Sie Abfahrtsinformationen für die gefundene Haltestelle ab
def get_departure_info(station_name):
    best_found_location = get_departures(station_name)
    if best_found_location:
        departures: List[Leg] = client.departures(
            station=best_found_location,
            date=datetime.datetime.now(),
            max_trips=15,
            products={
                'long_distance_express': True,
                'regional_express': True,
                'regional': True,
                'suburban': True,
                'bus': True,
                'ferry': True,
                'subway': True,
                'tram': True,
                'taxi': True
            }
        )
        return departures
    else:
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    departures = []
    station_name = ""

    # Get the station name from the cookie, if it exists
    if request.cookies.get('station_name'):
        station_name = request.cookies.get('station_name')

    if request.method == 'POST':
        station_name = request.form['station_name']
        departures = get_departure_info(station_name)

        # Set the station name cookie
        response = make_response(render_template('index.html', departures=departures, station_name=station_name))
        response.set_cookie('station_name', station_name)
        return response

    return render_template('index.html', departures=departures, station_name=station_name)

@app.route('/departures', methods=['GET'])
def departures():
  """
  Gibt die aktuellen Abfahrtsinformationen zurück.

  Returns:
    JSON-Objekt mit den Abfahrtsinformationen.
  """
  station_name=request.cookies.get('station_name')
  departures = client.departures(
    station=get_departures(station_name),
    date=datetime.datetime.now(),
    max_trips=15,
    products={
        'long_distance_express': True,
        'regional_express': True,
        'regional': True,
        'suburban': True,
        'bus': True,
        'ferry': True,
        'subway': True,
        'tram': True,
        'taxi': True
    }
  )

  # Konvertiere die Abfahrtsinformationen in ein JSON-Objekt
  departures_json = json.dumps([station_board_leg_to_dict(leg) for leg in departures])
  return departures_json

if __name__ == '__main__':
    app.run(debug=True)