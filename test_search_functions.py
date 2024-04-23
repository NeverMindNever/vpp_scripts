import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from search_functions import authenticate, search_flights  # Importing functions from search_functions.py


class TestFlightSearch(unittest.TestCase):

    @patch('search_functions.requests.post')
    def test_authentication_success(self, mock_post):
        # Mocking authentication response
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'access_token': 'mock_access_token'}

        # Running the function to test
        access_token = authenticate(client_id='mock_client_id', client_secret='mock_client_secret')

        # Assertion Test 1
        self.assertIsNotNone(access_token)
        self.assertEqual(access_token, 'mock_access_token')

    @patch('search_functions.requests.post')
    def test_authentication_failure(self, mock_post):
        # Mocking authentication response with failure
        mock_post.return_value.status_code = 401

        # Running the function to test
        access_token = authenticate(client_id='mock_client_id', client_secret='mock_client_secret')

        # Assertion Test 2
        self.assertIsNone(access_token)

    @patch('search_functions.requests.get')
    def test_search_flights_success(self, mock_get):
        # Mocking flight search response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'data': [
                {'type': 'flight-date', 'origin': 'CDG', 'destination': 'BCN', 'departureDate': '2024-06-27',
                 'returnDate': '2024-07-01', 'price': {'total': '216.77'}, 'links': {
                    'flightDestinations': 'https://test.api.amadeus.com/v1/shopping/flight-destinations?origin=PAR'
                                          '&departureDate=2024-06-01,'
                                          '2024-06-30&oneWay=false&duration=4&nonStop=false&maxPrice=250&currency=EUR'
                                          '&viewBy=DATE',
                    'flightOffers': 'https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode=PAR'
                                    '&destinationLocationCode=BCN&departureDate=2024-06-27&returnDate=2024-07-01'
                                    '&adults=1&nonStop=false&maxPrice=250&currency=EUR'}},
                {'type': 'flight-date', 'origin': 'CDG', 'destination': 'BCN', 'departureDate': '2024-06-21',
                 'returnDate': '2024-06-25', 'price': {'total': '216.77'}, 'links': {
                    'flightDestinations': 'https://test.api.amadeus.com/v1/shopping/flight-destinations?origin=PAR'
                                          '&departureDate=2024-06-01,'
                                          '2024-06-30&oneWay=false&duration=4&nonStop=false&maxPrice=250&currency=EUR'
                                          '&viewBy=DATE',
                    'flightOffers': 'https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode=PAR'
                                    '&destinationLocationCode=BCN&departureDate=2024-06-27&returnDate=2024-07-01'
                                    '&adults=1&nonStop=false&maxPrice=250&currency=EUR'}},
                {'type': 'flight-date', 'origin': 'CDG', 'destination': 'BCN', 'departureDate': '2024-06-06',
                 'returnDate': '2024-06-10', 'price': {'total': '216.77'}, 'links': {
                    'flightDestinations': 'https://test.api.amadeus.com/v1/shopping/flight-destinations?origin=PAR'
                                          '&departureDate=2024-06-01,'
                                          '2024-06-30&oneWay=false&duration=4&nonStop=false&maxPrice=250&currency=EUR'
                                          '&viewBy=DATE',
                    'flightOffers': 'https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode=PAR'
                                    '&destinationLocationCode=BCN&departureDate=2024-06-06&returnDate=2024-06-10'
                                    '&adults=1&nonStop=false&maxPrice=250&currency=EUR'}}

            ]
        }

        # Running the function to test
        flight = search_flights(
            origin='PAR',
            destination='BCN',
            start_date='2024-06-01',
            end_date='2024-06-30')

        # Assertion Test 3
        self.assertIsNotNone(flight)
        self.assertEqual(7, len(flight))
        self.assertEqual('2024-06-27', flight['departureDate'])
        self.assertEqual('2024-07-01', flight['returnDate'])

    @patch('search_functions.requests.get')
    def test_search_flights_failure(self, mock_get):
        # Mocking flight search response with failure
        mock_get.return_value.status_code = 404

        # Running the function to test
        flight = search_flights(origin='PAR', destination='BCN', start_date='2024-06-01', end_date='2024-06-30')

        # Assertion Test 4
        self.assertIsNone(flight)


if __name__ == '__main__':
    unittest.main()
