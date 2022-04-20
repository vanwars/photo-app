import utils
import requests

root_url = utils.root_url
import unittest

class TestCommentListEndpoint(unittest.TestCase):
    
    def setUp(self):
        self.current_user = utils.get_user_12()

    def test_comment_post_valid_request_201(self):
        post = utils.get_post_by_user(self.current_user.get('id'))
        body = {
            'post_id': post.get('id'),
            'text': 'Some comment text'
        }
        response = requests.post(root_url + '/api/comments', json=body)
        new_comment = response.json()
        self.assertEqual(response.status_code, 201)

        # check that the values are in the returned json:
        self.assertEqual(new_comment.get('post_id'), body.get('post_id'))
        self.assertEqual(new_comment.get('text'), body.get('text'))
        self.assertEqual(new_comment.get('user').get('id'), self.current_user.get('id'))

        # now delete comment from DB:
        utils.delete_comment_by_id(new_comment.get('id'))

        # and check that it's gone:
        self.assertEqual(utils.get_comment_by_id(new_comment.get('id')), [])


    def test_comment_post_invalid_post_id_format_400(self):
        body = {
            'post_id': 'dasdasdasd',
            'text': 'Some comment text'
        }
        response = requests.post(root_url + '/api/comments', json=body)
        # print(response.text)
        self.assertEqual(response.status_code, 400)

    def test_comment_post_invalid_post_id_404(self):
        body = {
            'post_id': 999999,
            'text': 'Some comment text'
        }
        response = requests.post(root_url + '/api/comments', json=body)
        # print(response.text)
        self.assertEqual(response.status_code, 404)

    def test_comment_post_unauthorized_post_id_404(self):
        post = utils.get_post_that_user_cannot_access(self.current_user.get('id'))
        body = {
            'post_id': post.get('id'),
            'text': 'Some comment text'
        }
        response = requests.post(root_url + '/api/comments', json=body)
        # print(response.text)
        self.assertEqual(response.status_code, 404)
    
    def test_comment_post_missing_text_400(self):
        post = utils.get_post_by_user(self.current_user.get('id'))
        body = {
            'post_id': post.get('id'),
        }
        response = requests.post(root_url + '/api/comments', json=body)
        # print(response.text)
        self.assertEqual(response.status_code, 400)
    

class TestCommentDetailEndpoint(unittest.TestCase):
    
    def setUp(self):
        self.current_user = utils.get_user_12()

    
    def test_comment_delete_valid_200(self):
        comment_to_delete = utils.get_comment_by_user(self.current_user.get('id'))
        comment_id =comment_to_delete.get('id')
        url = '{0}/api/comments/{1}'.format(root_url, comment_id)
        
        response = requests.delete(url)
        # print(response.text)
        self.assertEqual(response.status_code, 200)

        # restore the post in the database:
        utils.restore_comment_by_id(comment_to_delete)

    def test_comment_delete_invalid_id_format_404(self):
        url = '{0}/api/comments/sdfsdfdsf'.format(root_url)
        response = requests.delete(url)
        self.assertEqual(response.status_code, 404)

    def test_comment_delete_invalid_id_404(self):
        url = '{0}/api/comments/99999'.format(root_url)
        response = requests.delete(url)
        self.assertEqual(response.status_code, 404)

    def test_comment_delete_unauthorized_id_404(self):
        unauthorized_comment = utils.get_comment_that_user_cannot_delete(self.current_user.get('id'))
        url = '{0}/api/comments/{1}'.format(root_url, unauthorized_comment.get('id'))
        response = requests.delete(url)
        self.assertEqual(response.status_code, 404)



if __name__ == '__main__':
    # to run all of the tests:
    # unittest.main()

    # to run some of the tests (convenient for commenting out some of the tests):
    suite = unittest.TestSuite()
    suite.addTests([

        # POST Tests:
        TestCommentListEndpoint('test_comment_post_valid_request_201'),
        TestCommentListEndpoint('test_comment_post_invalid_post_id_format_400'),
        TestCommentListEndpoint('test_comment_post_invalid_post_id_404'),
        TestCommentListEndpoint('test_comment_post_unauthorized_post_id_404'),
        TestCommentListEndpoint('test_comment_post_missing_text_400'),

        # DELETE Tests:
        TestCommentDetailEndpoint('test_comment_delete_valid_200'),
        TestCommentDetailEndpoint('test_comment_delete_invalid_id_format_404'),
        TestCommentDetailEndpoint('test_comment_delete_invalid_id_404'),
        TestCommentDetailEndpoint('test_comment_delete_unauthorized_id_404'),
        
    ])

    unittest.TextTestRunner(verbosity=2).run(suite)