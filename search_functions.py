import requests
from datetime import datetime
from secrets import *


def authenticate(client_id=amadeus_client_id, client_secret=amadeus_client_secret):
    auth_url = "https://test.api.amadeus.com/v1/security/oauth2/token"

    # Payload for authentication
    auth_payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }

    # Requesting authentication token
    auth_response = requests.post(auth_url, data=auth_payload)

    # Extracting authentication token
    if auth_response.status_code == 200:
        return auth_response.json().get('access_token')
    else:
        # Handling unsuccessful authentication
        print(f"Authentication failed with status code: {auth_response.status_code}")
        return None


def search_flights(origin='PAR', destination='BCN', start_date='2024-03-01', end_date='2024-03-31'):
    access_token = authenticate(amadeus_client_id, amadeus_client_secret)
    if access_token:
        pass
    else:
        return None

    # API endpoint for flight search
    flight_search_url = "https://test.api.amadeus.com/v1/shopping/flight-dates"

    # Setting up headers for API requests
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Parameters for flight search
    flight_params = {
        'origin': origin,
        'destination': destination,
        'oneWay': False,
        'duration': 4,
        'nonStop': False,
        'maxPrice': 250,
        'currency': 'EUR',
        'viewBy': 'DATE',
        'departureDate': f'{start_date},{end_date}'
    }

    # Performing flight search
    response = requests.get(flight_search_url, headers=headers, params=flight_params)

    # Checking if request was successful
    if response.status_code == 200:
        # Extracting flight data from response
        flight_data = response.json().get('data')

        # Initializing list to store filtered flights
        filtered_flights = []

        # Filtering flights for Thursday departures
        for flight in flight_data:
            departure_date = datetime.strptime(flight.get('departureDate'), "%Y-%m-%d")
            if departure_date.weekday() == 3:  # Thursday is represented by 3
                return flight

    else:
        # Handling unsuccessful API request
        print(f"Flight search failed with status code: {response.status_code}")
        return None
