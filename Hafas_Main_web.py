from flask import Flask, render_template, request, make_response, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    station_name = request.cookies.get('station_name', '')  # Versuche, den Stationsnamen aus dem Cookie zu lesen
    departures = []

    if request.method == 'POST':
        station_name = request.form.get('station_name', '')
        if station_name:
            # Speichere den Stationsnamen im Cookie
            url = f"https://dbf.finalrewind.org/{station_name}.json?version=3"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                departures = data.get("departures", [])
                resp = make_response(render_template('index.html', station_name=station_name, departures=departures))
                resp.set_cookie('station_name', station_name)
                return resp

    if station_name:  # Überprüfe, ob ein Stationsname aus dem Cookie gelesen wurde
        url = f"https://dbf.finalrewind.org/{station_name}.json?version=3"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            departures = data.get("departures", [])

    return render_template('index.html', station_name=station_name, departures=departures)

@app.route('/update_departures', methods=['GET'])
def update_departures():
    station_name = request.cookies.get('station_name', '')
    departures = []

    if station_name:
        url = f"https://dbf.finalrewind.org/{station_name}.json?version=3"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            departures = data.get("departures", [])

    return jsonify({'departures': departures})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
