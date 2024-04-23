import unittest
from unittest.mock import patch, MagicMock
from wordpress_functions import get_categories_json, find_category_id_from_json


class TestWordPressFunctions(unittest.TestCase):

    @patch('wordpress_functions.requests.get')
    def test_get_categories_json_success(self, mock_get):
        # Mocking successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{'id': 1, 'name': 'Category1'}, {'id': 2, 'name': 'Category2'}]
        mock_get.return_value = mock_response

        # Running the function to test
        categories = get_categories_json()

        # Assertion Test 1
        self.assertIsNotNone(categories)
        self.assertEqual(len(categories), 2)
        self.assertEqual(categories[0]['name'], 'Category1')
        self.assertEqual(categories[1]['name'], 'Category2')

    @patch('wordpress_functions.requests.get')
    def test_get_categories_json_failure(self, mock_get):
        # Mocking failed response
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # Running the function to test
        categories = get_categories_json()

        # Assertion Test 2
        self.assertIsNotNone(categories)

    def test_find_category_id_from_json_found(self):
        # Running the function to test
        category_id = find_category_id_from_json(category_name='Mai')

        # Assertion Test 3
        self.assertEqual(15, category_id)

    def test_find_category_id_from_json_not_found(self):
        # Running the function to test with a category name not in the data
        category_id = find_category_id_from_json(category_name='NonExistentCategory')

        # Assertion Test 4
        self.assertIsNone(category_id)


if __name__ == '__main__':
    unittest.main()
