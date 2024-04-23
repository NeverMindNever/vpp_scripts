import requests
from datetime import datetime
import locale
from cities import cities
from constants import code
from cities import javascript_code
from search_functions import search_flights
from wordpress_functions import find_category_id_from_json
from wordpress_functions import wordpress_post








# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    origin = 'PAR'
    # Possible destinations : MIL, BCN, OPO
    destination = 'BCN'
    starting = '2024-06-01'
    ending = '2024-06-30'

    flight_found = search_flights(origin, destination, starting, ending)
    departure_airport = flight_found['origin']
    arrival_airport = flight_found['destination']
    start_date = flight_found['departureDate']
    end_date = flight_found['returnDate']
    price_flight = flight_found['price']['total']
    price_hotel = 326

    date_object = datetime.strptime(start_date, "%Y-%m-%d")

    # Set the locale to French
    locale.setlocale(locale.LC_TIME, 'fr_FR')

    month_name = date_object.strftime("%B")
    year = date_object.strftime("%Y")

    # Reset the locale to the default
    locale.setlocale(locale.LC_TIME, '')

    # Ajouter les catégories à l'article

    cities[destination]['categories'].append(find_category_id_from_json(month_name.capitalize()))
    cities[destination]['categories'].append(find_category_id_from_json(code[destination]['country'].capitalize()))

    # Définissez les données du nouvel article
    city_data = {
        'title': cities[destination]['title'].format(month_name=month_name, year=year),
        'slug': cities[destination]['slug'].format(month_name=month_name, year=year),
        'categories': cities[destination]['categories'],
        'tags': cities[destination]['tags'],
        'author': cities[destination]['author'],
        'featured_media': cities[destination]['featured_media'],
        'content': cities[destination]['content'].format(start_date=start_date, end_date=end_date,
                                                         price_flight=price_flight, departure_airport=departure_airport,
                                                         arrival_airport=arrival_airport,
                                                         departure_city=code[origin]['name'],
                                                         departure_country=code[origin]['country'],
                                                         price_hotel=price_hotel,
                                                         month_name=month_name,
                                                         year=year
                                                         ) + javascript_code,
        'status': 'draft',
    }

    #Call word prod post API
    wordpress_post(city_data)
