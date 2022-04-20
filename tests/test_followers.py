import utils
import requests

root_url = utils.root_url
import unittest

class TestFollowerListEndpoint(unittest.TestCase):
    
    def setUp(self):
        self.current_user = utils.get_user_12()
        pass

    def test_followers_get(self):
        response = requests.get('{0}/api/followers'.format(root_url))
        follower_list = response.json()
        self.assertEqual(response.status_code, 200)

        authorized_user_ids = utils.get_follower_ids(self.current_user.get('id'))
        
        self.assertTrue(len(authorized_user_ids) > 0)
        self.assertEqual(len(authorized_user_ids), len(follower_list))
        
        # make sure that every follower retrieved from the endpoint
        # is authorized:
        for entry in follower_list:
            # print(entry, authorized_user_ids)
            self.assertTrue(entry.get('follower').get('id') in authorized_user_ids)

    def test_follower_get_check_data_structure(self):
        response = requests.get('{0}/api/followers'.format(root_url))
        self.assertEqual(response.status_code, 200)
        following_list = response.json()
       
        entry = following_list[0]
        self.assertTrue('id' in entry and type(entry['id']) == int)
        self.assertTrue('follower' in entry and type(entry['follower']) == dict)
        follower = entry.get('follower')
        self.assertTrue('id' in follower and type(follower['id']) == int)
        self.assertTrue('first_name' in follower and type(follower['first_name']) in [str, type(None)])
        self.assertTrue('last_name' in follower and type(follower['last_name']) in [str, type(None)])
        self.assertTrue('image_url' in follower and type(follower['image_url']) in [str, type(None)])
        self.assertTrue('thumb_url' in follower and type(follower['thumb_url']) in [str, type(None)])
     
   

if __name__ == '__main__':
    # to run all of the tests:
    # unittest.main()

    # to run some of the tests (convenient for commenting out some of the tests):
    suite = unittest.TestSuite()
    suite.addTests([
        TestFollowerListEndpoint('test_followers_get'),                       
        TestFollowerListEndpoint('test_follower_get_check_data_structure')
        
    ])

    unittest.TextTestRunner(verbosity=2).run(suite)