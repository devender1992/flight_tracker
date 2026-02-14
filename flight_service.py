import requests
import os
import random

class FlightService:
    def __init__(self):
        self.api_key = os.getenv('AVIATION_STACK_API_KEY')
        self.base_url = "http://api.aviationstack.com/v1"

    def _enrich_flight_data(self, flight):
        """Enrich flight data with mock prices and missing details."""
        # Mock Fare Info
        if 'ticket_price' not in flight:
            flight['ticket_price'] = random.randint(150, 1200)
            flight['ticket_class'] = random.choice(['Economy', 'Business', 'First Class'])
        
        # Mock Terminal/Gate if missing
        if not flight.get('departure', {}).get('gate'):
            if 'departure' not in flight: flight['departure'] = {}
            flight['departure']['gate'] = f"{random.choice(['A','B','C'])}{random.randint(1, 30)}"
            flight['departure']['terminal'] = f"{random.randint(1, 5)}"
            
        if not flight.get('arrival', {}).get('gate'):
             if 'arrival' not in flight: flight['arrival'] = {}
             flight['arrival']['gate'] = f"{random.choice(['D','E','F'])}{random.randint(1, 30)}"
             flight['arrival']['terminal'] = f"{random.randint(1, 5)}"
             flight['arrival']['baggage'] = f"{random.randint(1, 10)}"

        return flight

    def get_flights(self, origin, destination):
        params = {
            'access_key': self.api_key,
            'dep_iata': origin,
            'arr_iata': destination
        }
        try:
            response = requests.get(f"{self.base_url}/flights", params=params)
            response.raise_for_status()
            data = response.json()
            flights = data.get('data', [])
            
            # Enrich with mock data
            for flight in flights:
                self._enrich_flight_data(flight)
                
            return flights
        except requests.exceptions.RequestException as e:
            print(f"Error fetching flights: {e}")
            return []

    def get_flight_status(self, flight_number):
        params = {
            'access_key': self.api_key,
            'flight_iata': flight_number
        }
        try:
            response = requests.get(f"{self.base_url}/flights", params=params)
            response.raise_for_status()
            data = response.json()
            results = data.get('data', [])
            if results:
                flight = results[0]
                return self._enrich_flight_data(flight)
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching flight status: {e}")
            return None
