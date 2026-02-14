from flask import Flask, render_template, request
from flight_service import FlightService
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
flight_service = FlightService()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search_flights():
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    flights = flight_service.get_flights(origin, destination)
    return render_template('results.html', flights=flights)

@app.route('/status')
def flight_status():
    flight_number = request.args.get('flight_number')
    status = flight_service.get_flight_status(flight_number)
    return render_template('status.html', status=status)

if __name__ == '__main__':
    app.run(debug=True)
