import utils
import requests

root_url = utils.root_url
import unittest

class TestStoryListEndpoint(unittest.TestCase):
    
    def setUp(self):
        self.current_user = utils.get_user_12()
        pass

    def test_stories_get_check_if_query_correct(self):
        response = requests.get('{0}/api/stories'.format(root_url))
        stories = response.json()
        self.assertEqual(response.status_code, 200)

        authorized_user_ids = utils.get_authorized_user_ids(self.current_user.get('id'))
        story_ids = utils.get_stories_by_user(self.current_user.get('id'))
        self.assertTrue(len(stories) > 1)
        self.assertEqual(len(story_ids), len(stories))
        for story in stories:
            self.assertTrue(story.get('user').get('id') in authorized_user_ids)
            self.assertTrue(story.get('id') in story_ids)

    def test_stories_get_check_data_structure(self):
        response = requests.get('{0}/api/stories'.format(root_url))
        self.assertEqual(response.status_code, 200)
        stories = response.json()
       
        story = stories[0]
        self.assertTrue('id' in story and type(story['id']) == int)
        self.assertTrue('user' in story and type(story['user']) == dict)
        self.assertTrue('text' in story and type(story['text']) == str)
        user = story.get('user')
        self.assertTrue('id' in user and type(user['id']) == int)
        self.assertTrue('first_name' in user and type(user['first_name']) in [str, type(None)])
        self.assertTrue('last_name' in user and type(user['last_name']) in [str, type(None)])
        self.assertTrue('image_url' in user and type(user['image_url']) in [str, type(None)])
        self.assertTrue('thumb_url' in user and type(user['thumb_url']) in [str, type(None)])
     
   

if __name__ == '__main__':
    # to run all of the tests:
    # unittest.main()

    # to run some of the tests (convenient for commenting out some of the tests):
    suite = unittest.TestSuite()
    suite.addTests([
        TestStoryListEndpoint('test_stories_get_check_if_query_correct'),                       
        TestStoryListEndpoint('test_stories_get_check_data_structure')
        
    ])

    unittest.TextTestRunner(verbosity=2).run(suite)