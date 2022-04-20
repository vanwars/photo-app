import utils
import requests

root_url = utils.root_url
import unittest

class TestFollowingListEndpoint(unittest.TestCase):
    
    def setUp(self):
        self.current_user = utils.get_user_12()

    def test_following_get_check_data_structure(self):
        response = requests.get('{0}/api/following'.format(root_url))
        self.assertEqual(response.status_code, 200)
        following_list = response.json()
       
        entry = following_list[0]
        self.assertTrue('id' in entry and type(entry['id']) == int)
        self.assertTrue('following' in entry and type(entry['following']) == dict)
        following = entry.get('following')
        self.assertTrue('id' in following and type(following['id']) == int)
        self.assertTrue('first_name' in following and type(following['first_name']) in [str, type(None)])
        self.assertTrue('last_name' in following and type(following['last_name']) in [str, type(None)])
        self.assertTrue('image_url' in following and type(following['image_url']) in [str, type(None)])
        self.assertTrue('thumb_url' in following and type(following['thumb_url']) in [str, type(None)])
        

    def test_following_get_check_if_query_correct(self):
        response = requests.get('{0}/api/following'.format(root_url))
        following_list = response.json()
        self.assertEqual(response.status_code, 200)

        # check that these are actually the people you're following:
        authorized_user_ids = utils.get_following_ids(self.current_user.get('id'))
        self.assertTrue(len(authorized_user_ids) > 1)
        self.assertEqual(len(authorized_user_ids), len(following_list))
        for entry in following_list:
            # print(entry, authorized_user_ids)
            self.assertTrue(entry.get('following').get('id') in authorized_user_ids)
   

    def test_following_post_valid_request_201(self):
        user = utils.get_unfollowed_user(self.current_user.get('id'))
        body = {
            'user_id': user.get('id')
        }
        response = requests.post(root_url + '/api/following', json=body)
        # print(response.text)
        self.assertEqual(response.status_code, 201)
        new_person_to_follow = response.json()
        following = new_person_to_follow.get('following')

        self.assertEqual(user.get('id'), following.get('id'))
        self.assertEqual(user.get('first_name'), following.get('first_name'))
        self.assertEqual(user.get('last_name'), following.get('last_name'))
        self.assertEqual(user.get('username'), following.get('username'))
        self.assertEqual(user.get('email'), following.get('email'))
        self.assertEqual(user.get('image_url'), following.get('image_url'))
        self.assertEqual(user.get('thumb_url'), following.get('thumb_url'))

        # check that the record is in the database:get_following_record_by_id
        db_rec = utils.get_following_by_id(new_person_to_follow.get('id'))
        self.assertEqual(db_rec.get('id'), new_person_to_follow.get('id'))
       
        # now delete following record from DB:
        utils.delete_following_by_id(new_person_to_follow.get('id'))

        # and check that it's gone:
        db_rec = utils.get_following_by_id(new_person_to_follow.get('id'))
        self.assertEqual(db_rec, [])

    def test_following_post_no_duplicates_400(self):
        already_following = utils.get_following_by_user(self.current_user.get('id'))
        body = {
            'user_id': already_following.get('following_id')
        }
        response = requests.post(root_url + '/api/following', json=body)
        # print(response.text)
        self.assertEqual(response.status_code, 400)

    def test_following_post_invalid_user_id_format_400(self):
        body = {
            'user_id': 'dasdasdasd'
        }
        response = requests.post(root_url + '/api/following', json=body)
        # print(response.text)
        self.assertEqual(response.status_code, 400)

    def test_following_post_invalid_user_id_404(self):
        body = {
            'user_id': 999999,
        }
        response = requests.post(root_url + '/api/following', json=body)
        # print(response.text)
        self.assertEqual(response.status_code, 404)
    
    def test_following_post_missing_user_id_400(self):
        response = requests.post(root_url + '/api/following', json={})
        # print(response.text)
        self.assertEqual(response.status_code, 400)
    
class TestFollowingDetailEndpoint(unittest.TestCase):
    
    def setUp(self):
        self.current_user = utils.get_user_12()

    
    def test_following_delete_valid_200(self):
        following_to_delete = utils.get_following_by_user(self.current_user.get('id'))
        following_id = following_to_delete.get('id')
        url = '{0}/api/following/{1}'.format(root_url, following_id)
        
        response = requests.delete(url)
        # print(response.text)
        self.assertEqual(response.status_code, 200)

        # check that it's really deleted:
        following_db = utils.get_following_by_id(following_id)
        self.assertEqual(following_db, [])

        # restore the post in the database:
        utils.restore_following(following_to_delete)


    def test_following_delete_invalid_id_format_404(self):
        url = '{0}/api/following/sdfsdfdsf'.format(root_url)
        response = requests.delete(url)
        self.assertEqual(response.status_code, 404)
        
    
    def test_following_delete_invalid_id_404(self):
        url = '{0}/api/following/99999'.format(root_url)
        response = requests.delete(url)
        self.assertEqual(response.status_code, 404)

        
    def test_following_delete_unauthorized_id_404(self): 
        unauthorized_following = utils.get_following_that_user_cannot_delete(self.current_user.get('id'))
        url = '{0}/api/following/{1}'.format(root_url, unauthorized_following.get('id'))
        response = requests.delete(url)
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    # to run all of the tests:
    # unittest.main()

    # to run some of the tests (convenient for commenting out some of the tests):
    suite = unittest.TestSuite()
    suite.addTests([

        # GET (List)
        TestFollowingListEndpoint('test_following_get_check_data_structure'),   
        TestFollowingListEndpoint('test_following_get_check_if_query_correct'),

        # POST
        TestFollowingListEndpoint('test_following_post_valid_request_201'),
        TestFollowingListEndpoint('test_following_post_no_duplicates_400'),
        TestFollowingListEndpoint('test_following_post_invalid_user_id_format_400'),
        TestFollowingListEndpoint('test_following_post_invalid_user_id_404'),
        TestFollowingListEndpoint('test_following_post_missing_user_id_400'), 

        # DELETE
        TestFollowingDetailEndpoint('test_following_delete_valid_200'),
        TestFollowingDetailEndpoint('test_following_delete_invalid_id_format_404'),
        TestFollowingDetailEndpoint('test_following_delete_invalid_id_404'),
        TestFollowingDetailEndpoint('test_following_delete_unauthorized_id_404') 
    ])

    unittest.TextTestRunner(verbosity=2).run(suite)