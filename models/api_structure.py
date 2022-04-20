import json
from models import Post, Comment, Bookmark, Following, db, LikePost
from views import get_authorized_user_ids

class ApiNavigator(object):
    def __init__(self, current_user):
        self.current_user = current_user
        self.post = Post.query.filter_by(
                user_id=self.current_user.id
            ).limit(1).one()
        self.comment = Comment.query.filter_by(
                user_id=self.current_user.id
            ).limit(1).one()
        self.following = Following.query.filter_by(
                user_id=self.current_user.id
            ).limit(1).one()
        self.get_user_id_to_follow = self.get_user_id_to_follow()
        self.unbookmarked_post_id = self.get_unbookmarked_post_id()
        self.bookmark = Bookmark.query.filter_by(
                user_id=self.current_user.id
            ).limit(1).one()
        self.unliked_post_id = self.get_unliked_post_id()
        self.like = LikePost.query.filter_by(
                user_id=self.current_user.id
            ).limit(1).one()
        self.image_url = 'https://picsum.photos/300/300'
        # image_url = 'https://media.gettyimages.com/photos/happy-dog-picture-id182176638'
       

    def get_user_id_to_follow(self):
        sql = '''
            SELECT users.id
            FROM users
            WHERE id NOT IN (
                SELECT f.following_id 
                FROM following f
                WHERE f.user_id = {user_id} 
            )
            LIMIT 1
        '''.format(user_id=self.current_user.id)
        rows = list(db.engine.execute(sql))
        return rows[0][0]

    def get_unbookmarked_post_id(self):
        ids = get_authorized_user_ids(self.current_user)
        sql = '''
            SELECT p.id 
            FROM posts p
            WHERE p.id NOT IN (
                    -- posts that are already bookmarked:
                    SELECT post_id from bookmarks where user_id={user_id}
                )
                AND p.id IN (
                    -- posts the current user can access:
                    SELECT id from posts where user_id IN ({authorized_user_ids})
                )
            LIMIT 1
        '''.format(
                user_id=self.current_user.id,
                authorized_user_ids=', '.join([str(id) for id in ids])
            )
        rows = list(db.engine.execute(sql))
        return rows[0][0]


    def get_unliked_post_id(self):
        ids = get_authorized_user_ids(self.current_user)
        sql = '''
            SELECT p.id 
            FROM posts p
            WHERE p.id NOT IN (
                    -- posts that are already bookmarked:
                    SELECT post_id from likes_posts where user_id={user_id}
                )
                AND p.id IN (
                    -- posts the current user can access:
                    SELECT id from posts where user_id IN ({authorized_user_ids})
                )
            LIMIT 1
        '''.format(
                user_id=self.current_user.id,
                authorized_user_ids=', '.join([str(id) for id in ids])
            )
        rows = list(db.engine.execute(sql))
        return rows[0][0]

    def get_endpoints(self):
        return {
            'Posts': [
                {
                    'id': 'posts-get',
                    'name': 'Get List of Posts',
                    'endpoint': '/api/posts/',
                    'endpoint_example': '/api/posts/?limit=3',
                    'method': 'GET',
                    'request_description': 'Retrieves a list of posts that the current user can access. This includes posts created by the current user, as well as posts of users that the current user is following.',
                    'response_description': 'List of post objects that are accessible to the current user.',
                    'response_type': 'List<Post>',
                    'parameters': [
                        {
                            'name': 'limit',
                            'data_type': 'int',
                            'optional_or_required': 'optional',
                            'description': 'Limits the number of posts returned (defaults to 10, maximum is 50).'
                        }
                    ]
                },
                {
                    'id': 'post-get',
                    'name': 'Get Single Post',
                    'endpoint': '/api/posts/<id>',
                    'endpoint_example': '/api/posts/{0}'.format(self.post.id),
                    'method': 'GET',
                    'request_description': 'Retrieves the post matching the id from the URL request.',
                    'response_description': 'Post object requested.',
                    'response_type': 'Post',
                    'parameters': []
                },
                {
                    'id': 'post-add',
                    'name': 'Add New Post',
                    'endpoint': '/api/posts/',
                    'endpoint_example': '/api/posts/',
                    'method': 'POST',
                    'request_description': 'Creates a new post from the data that you send via the request body.',
                    'response_description': 'The Post object you just created.',
                    'response_type': 'Post',
                    'parameters': [
                        {
                            'name': 'image_url',
                            'data_type': 'string',
                            'optional_or_required': 'required',
                            'description': 'A URL path to the image you want to post.'
                        },
                        {
                            'name': 'caption',
                            'data_type': 'string',
                            'optional_or_required': 'optional',
                            'description': 'A message that you want to associate with your post.'
                        },
                        {
                            'name': 'alt_text',
                            'data_type': 'string',
                            'optional_or_required': 'optional',
                            'description': 'A description of the image you posted.'
                        }
                    ],
                    'sample_body': json.dumps({
                        'image_url': self.image_url,
                        'caption': 'Pretty landscape',
                        'alt_text': 'The photo shows a picture of a canyon taken in Sedona, AZ',
                    }, indent=4)
                },
                {
                    'id': 'post-update',
                    'name': 'Update Post',
                    'endpoint': '/api/posts/<id>',
                    'endpoint_example': '/api/posts/{0}'.format(self.post.id),
                    'method': 'PATCH',
                    'request_description': 'Updates the post from the data you send via the request body.',
                    'response_description': 'The Post object you just updated.',
                    'response_type': 'Post',
                    'parameters': [
                        {
                            'name': 'image_url',
                            'data_type': 'string',
                            'optional_or_required': 'optional',
                            'description': 'A URL path to the image you want to post.'
                        },
                        {
                            'name': 'caption',
                            'data_type': 'string',
                            'optional_or_required': 'optional',
                            'description': 'A message that you want to associate with your post.'
                        },
                        {
                            'name': 'alt_text',
                            'data_type': 'string',
                            'optional_or_required': 'optional',
                            'description': 'A description of the image you posted.'
                        }
                    ],
                    'sample_body': json.dumps({
                        'image_url': self.image_url,
                        'caption': 'New caption',
                        'alt_text': 'New alt text',
                    }, indent=4)
                },
                {
                    'id': 'post-delete',
                    'name': 'Delete Post',
                    'endpoint': '/api/posts/<id>',
                    'endpoint_example': '/api/posts/{0}'.format(self.post.id),
                    'method': 'DELETE',
                    'request_description': 'Deletes the specified post.',
                    'response_description': 'A success message indicating that the post has been deleted.',
                    'response_type': 'Message',
                    'parameters': []
                }
            ],
            'Comments': [
                {
                    'id': 'comment-post',
                    'name': 'Add Comment',
                    'endpoint': '/api/comments',
                    'endpoint_example': '/api/comments',
                    'method': 'POST',
                    'request_description': 'Creates a new comment.',
                    'response_description': 'Comment object.',
                    'response_type': 'Comment',
                    'parameters': [
                        {
                            'name': 'post_id',
                            'data_type': 'int',
                            'optional_or_required': 'required',
                            'description': 'The id of the Post that the comment references.'
                        },
                        {
                            'name': 'text',
                            'data_type': 'string',
                            'optional_or_required': 'required',
                            'description': 'The text of the comment.'
                        }
                    ],
                    'sample_body': json.dumps({
                        'post_id': self.post.id,
                        'text': 'Some comment text text text.',
                    }, indent=4)
                },
                {
                    'id': 'comment-delete',
                    'name': 'Delete Comment',
                    'endpoint': '/api/comments/<id>',
                    'endpoint_example': '/api/comments/{0}'.format(self.comment.id),
                    'method': 'DELETE',
                    'request_description': 'Deletes a comment',
                    'response_description': 'Message indicating whether or not the delete was successful.',
                    'response_type': 'Message',
                    'parameters': []
                }
            ],
            'Followers': [
                {
                    'id': 'followers',
                    'name': 'Get Followers',
                    'endpoint': '/api/followers/',
                    'endpoint_example': '/api/followers/',
                    'method': 'GET',
                    'request_description': 'Retrieves all of the users who are following you.',
                    'response_description': 'A list of your followers',
                    'response_type': 'List<Follower>',
                    'parameters': []
                }
            ],
            'Following': [
                {
                    'id': 'following-get',
                    'name': 'Get Users You Follow',
                    'endpoint': '/api/following/',
                    'endpoint_example': '/api/following/',
                    'method': 'GET',
                    'request_description': 'Retrieves all of the users who you follow.',
                    'response_description': 'A list of users you are following.',
                    'response_type': 'List<Following>',
                    'parameters': []
                },
                {
                    'id': 'following-post',
                    'name': 'Follow New User',
                    'endpoint': '/api/following/',
                    'endpoint_example': '/api/following/',
                    'method': 'POST',
                    'request_description': 'Creates a new following instance.',
                    'response_description': 'Following object.',
                    'response_type': 'Following',
                    'parameters': [
                        {
                            'name': 'user_id',
                            'data_type': 'int',
                            'optional_or_required': 'required',
                            'description': 'The id of the User that you would like to follow.'
                        }
                    ],
                    'sample_body': json.dumps({
                        'user_id': self.get_user_id_to_follow
                    }, indent=4)
                },
                {
                    'id': 'following-delete',
                    'name': 'Unfollow User',
                    'endpoint': '/api/following/<id>',
                    'endpoint_example': '/api/following/{0}'.format(self.following.id),
                    'method': 'DELETE',
                    'request_description': 'Deletes a following instance.',
                    'response_description': 'Message.',
                    'response_type': 'Message'
                }
            ],
            'Profile': [
                {
                    'id': 'profile',
                    'name': 'Get Your Profile',
                    'endpoint': '/api/profile/',
                    'endpoint_example': '/api/profile/',
                    'method': 'GET',
                    'request_description': 'Retrieves your user profile.',
                    'response_description': 'Your profile',
                    'response_type': 'User',
                    'parameters': []
                }
            ],
            'Suggestions': [
                {
                    'id': 'suggestions',
                    'name': 'Get Follow Suggestions',
                    'endpoint': '/api/suggestions/',
                    'endpoint_example': '/api/suggestions/',
                    'method': 'GET',
                    'request_description': 'Retrieves list of suggested user accounts that you may be interested in following.',
                    'response_description': 'List of user accounts.',
                    'response_type': 'List<User>',
                    'parameters': []
                }
            ],
            'Stories': [
                {
                    'id': 'stories',
                    'name': 'Get Your Stories',
                    'endpoint': '/api/stories/',
                    'endpoint_example': '/api/stories/',
                    'method': 'GET',
                    'request_description': 'Retrieves a list of stories posted by people in your network.',
                    'response_description': 'List of stories.',
                    'response_type': 'List<Story>',
                    'parameters': []
                }
            ],
            'Bookmarks': [
                {
                    'id': 'bookmarks-get',
                    'name': 'Get Your Bookmarks',
                    'endpoint': '/api/bookmarks/',
                    'endpoint_example': '/api/bookmarks/',
                    'method': 'GET',
                    'request_description': 'Retrieves a list of posts you have bookmarked.',
                    'response_description': 'List of bookmarks.',
                    'response_type': 'List<Bookmark>',
                    'parameters': []
                },
                {
                    'id': 'bookmarks-post',
                    'name': 'Create New Bookmarks',
                    'endpoint': '/api/bookmarks/',
                    'endpoint_example': '/api/bookmarks/',
                    'method': 'POST',
                    'request_description': 'Bookmarks a Post.',
                    'response_description': 'Bookmark object.',
                    'response_type': 'Bookmark',
                    'parameters': [
                        {
                            'name': 'post_id',
                            'data_type': 'int',
                            'optional_or_required': 'required',
                            'description': 'The id of the Post that you would like to bookmark.'
                        }
                    ],
                    'sample_body': json.dumps({
                        'post_id': self.unbookmarked_post_id
                    }, indent=4)
                },
                {
                    'id': 'bookmarks-delete',
                    'name': 'Remove Bookmark',
                    'endpoint': '/api/bookmarks/<id>',
                    'endpoint_example': '/api/bookmarks/{0}'.format(self.bookmark.id),
                    'method': 'DELETE',
                    'request_description': 'Remove a bookmark.',
                    'response_description': 'Message indicating whether or not the Bookmark was successfully removed.',
                    'response_type': 'Message'
                }
            ],
            'Post Likes': [
                {
                    'id': 'likes-post',
                    'name': 'Add a Like',
                    'endpoint': '/api/posts/likes/',
                    'endpoint_example': '/api/posts/likes/'.format(post_id=self.unliked_post_id),
                    'method': 'POST',
                    'request_description': 'Ensure that the post id of the Post that you want to like is included in the endpoint url (see example below).',
                    'response_description': 'The Like object.',
                    'response_type': 'List',
                    'parameters': [
                        {
                            'name': 'post_id',
                            'data_type': 'int',
                            'optional_or_required': 'required',
                            'description': 'The id of the Post that you would like to like.'
                        }
                    ],
                    'sample_body': json.dumps({
                        'post_id': self.unliked_post_id
                    }, indent=4)
                },
                {
                    'id': 'likes-delete',
                    'name': 'Remove a Like',
                    'endpoint': '/api/posts/likes/<id>',
                    'endpoint_example': '/api/posts/likes/{id}'.format(id=self.like.id),
                    'method': 'DELETE',
                    'request_description': 'Ask to remove a like.',
                    'response_description': 'A message indicating whether or not the Like was successfully removed/',
                    'response_type': 'Message'
                }
            ]
        }