import utils
import requests

import unittest

root_url = utils.root_url
class TestSuggestionsEndpoint(unittest.TestCase):
    
    def setUp(self):
        self.current_user = utils.get_user_12()
        pass

    def test_suggestions_get_check_if_query_correct(self):
        response = requests.get('{0}/api/suggestions'.format(root_url))
        self.assertEqual(response.status_code, 200)
        suggestions = response.json()
        ids = utils.get_unrelated_users(self.current_user.get('id'))
        self.assertEqual(len(suggestions), 7)
        for suggestion in suggestions:
            # print(suggestion.get('id'), ids)
            self.assertTrue(suggestion.get('id') in ids)


    def test_suggestions_get_check_if_data_structure_correct(self):
        response = requests.get('{0}/api/suggestions'.format(root_url))
        self.assertEqual(response.status_code, 200)
        suggestions = response.json()
        suggestion = suggestions[0]
        user = utils.get_user(suggestion.get('id'))

        self.assertEqual(suggestion.get('id'), user.get('id'))
        self.assertEqual(suggestion.get('first_name'), user.get('first_name'))
        self.assertEqual(suggestion.get('last_name'), user.get('last_name'))
        self.assertEqual(suggestion.get('username'), user.get('username'))
        self.assertEqual(suggestion.get('email'), user.get('email'))
        self.assertEqual(suggestion.get('image_url'), user.get('image_url'))
        self.assertEqual(suggestion.get('thumb_url'), user.get('thumb_url'))

if __name__ == '__main__':
    # to run all of the tests:
    # unittest.main()

    # to run some of the tests (convenient for commenting out some of the tests):
    suite = unittest.TestSuite()
    suite.addTests([
        TestSuggestionsEndpoint('test_suggestions_get_check_if_query_correct'),
        TestSuggestionsEndpoint('test_suggestions_get_check_if_data_structure_correct')        
    ])

    unittest.TextTestRunner(verbosity=2).run(suite)