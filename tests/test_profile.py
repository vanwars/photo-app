import utils
import requests

root_url = utils.root_url
import unittest

class TestProfileEndpoint(unittest.TestCase):
    
    def setUp(self):
        self.current_user = utils.get_user_12()
        pass

    def test_profile_get_check_if_query_correct(self):
        response = requests.get('{0}/api/profile'.format(root_url))
        profile = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(profile.get('id'), self.current_user.get('id'))
        self.assertEqual(profile.get('first_name'), self.current_user.get('first_name'))
        self.assertEqual(profile.get('last_name'), self.current_user.get('last_name'))
        self.assertEqual(profile.get('username'), self.current_user.get('username'))
        self.assertEqual(profile.get('email'), self.current_user.get('email'))
        self.assertEqual(profile.get('image_url'), self.current_user.get('image_url'))
        self.assertEqual(profile.get('thumb_url'), self.current_user.get('thumb_url'))


if __name__ == '__main__':
    # to run all of the tests:
    # unittest.main()

    # to run some of the tests (convenient for commenting out some of the tests):
    suite = unittest.TestSuite()
    suite.addTests([
        TestProfileEndpoint('test_profile_get_check_if_query_correct')        
    ])

    unittest.TextTestRunner(verbosity=2).run(suite)