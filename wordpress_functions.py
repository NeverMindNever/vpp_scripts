import requests
from secrets import *

# Define the WordPress API endpoint
base_url = "https://voyages-a-petits-prix.fr/wp-json/wp/v2"
token_url = "https://voyages-a-petits-prix.fr/wp-json/jwt-auth/v1/token"

# Spécifiez l'URL de base de votre site WordPress et l'endpoint pour créer un nouvel article
endpoint = '/posts'


def authenticate(username=wordpress_username, password=wordpress_password, token_url=token_url):
    # Define the authentication body with the provided username and password
    auth_body = {
        "username": username,
        "password": password
    }

    try:
        # Send a POST request to the token URL with the authentication body
        response = requests.post(token_url, data=auth_body)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract and return the authentication token from the response
            token = response.json().get("token")
            return token
        else:
            # If the request was not successful, print the error message
            print(f"Authentication failed with status code: {response.status_code}")
            return None
    except Exception as e:
        # If an exception occurs during the request, print the error message
        print(f"An error occurred during authentication: {e}")
        return None


def wordpress_post(city_data):
    # Ajoutez des en-têtes pour spécifier que vous envoyez des données JSON
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {authenticate()}",
    }

    # Envoyer une requête POST à l'API WordPress pour créer un nouvel article
    response = requests.post(base_url + endpoint, json=city_data, headers=headers)
    # Verifier si la réponse est correcte
    if response.status_code == 201:
        print('Article publié avec succès.')
    else:
        print('Erreur lors de la publication de l\'article.')
        print(response.status_code)


def get_categories_json():
    """Retrieve categories data from the API."""
    endpoint = "https://voyages-a-petits-prix.fr/wp-json/wp/v2/categories"
    params = {'per_page': 100}
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching categories data: {e}")
        return None


def find_category_id_from_json(category_name='Mai'):
    """
    Find category ID based on category name from JSON data.

    :param category_name: The name of the category to search for.
    :return: The ID of the category if found, None otherwise.
    """
    categories_json = get_categories_json()
    if categories_json is None:
        return None

    for cat in categories_json:
        if cat.get('name') == category_name:
            return cat.get('id')
    return None  # Return None if the category is not found
