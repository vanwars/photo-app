from models import db, User, Post, Comment,  LikeComment, \
    LikePost, Bookmark, Following, Story
import os
import random
from flask import Flask
from faker import Faker
from datetime import datetime, timedelta

from dotenv import load_dotenv
load_dotenv()

fake = Faker()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# global variables to keep track of what got created and for whom
users = []
posts = []
comments = []
ppl_user_is_following_map = {}

def generate_image(id:int=None, width:int=300, height:int=200):
    '''
    Generates fake image:
        * id (int): image identifier
        * width (int): width of the pic
        * height (int): height of the pic
    Returns an image url.
    '''
    image_id = id or random.randint(0, 1000)
    return 'https://picsum.photos/{w}/{h}?id={id}'.format(
        id=image_id, w=width, h=height
    )

def _create_webdev_user():
    # 1. generate fake user data
    first_name = 'Webdev'
    last_name = 'User'
    username = 'webdev'
    email = 'webdev@u.northwestern.edu'
    
    # 2. create a new user (DB object)
    user = User(first_name, last_name, username, email,
        image_url=generate_image(),
        thumb_url= generate_image(width=30, height=30)
    )
    # 3. generate encrypted password:
    user.password_plaintext = 'password'
    user.set_password(user.password_plaintext)
    return user

def _create_user():
    # 1. generate fake user data
    profile = fake.simple_profile()
    tokens = profile['name'].split(' ')
    first_name = tokens.pop(0)
    last_name = ' '.join(tokens)
    username = '{0}_{1}'.format(first_name, last_name.replace(' ', '_')).lower()
    provider = profile['mail'].split('@')[1]
    email = '{0}@{1}'.format(username, provider)
    
    # 2. create a new user (DB object)
    user = User(first_name, last_name, username, email,
        image_url=generate_image(),
        thumb_url= generate_image(width=30, height=30)
    )
    # generate fake password. In reality, never store passwords
    # in plaintext, but useful when we're testing...
    user.password_plaintext = fake.sentence(nb_words=3).replace(' ', '_').replace('.', '').lower()
    
    # encrypt fake password (how you should actually do it)...
    user.set_password(user.password_plaintext) # encrypts password
    return user

def _create_post(user):
    time_of_post = datetime.now() - timedelta(hours=random.randint(1, 100))
    return Post(
        generate_image(width=600, height=430),
        user.id, 
        caption=fake.sentence(nb_words=random.randint(15, 50)),
        pub_date=time_of_post
    )

def _create_story(user):
    time_of_post = datetime.now() - timedelta(hours=random.randint(1, 100))
    return Story(
        fake.sentence(nb_words=random.randint(10, 30)), 
        user.id,
        pub_date=time_of_post
    )
    

def _create_post_likes(post, follower_ids):
    user_ids = follower_ids.copy() 
    # only followers of the current user (or the current user) can like
    # the user's post:
    # print('Creating post likes...')
    for _ in range(random.randint(0, 5)):
        i = random.randint(0, len(user_ids) - 1)
        user_id = user_ids.pop(i)
        like = LikePost(user_id, post.id)
        db.session.add(like)
        if len(user_ids) == 0:
            break

def _create_post_bookmarks(post, follower_ids):
    for _ in range(random.randint(0, 4)):
        i = random.randint(0, len(follower_ids) - 1)
        user_id = follower_ids.pop(i)
        bookmark = Bookmark(user_id, post.id)
        db.session.add(bookmark)
        if len(follower_ids) == 0:
            break


def _create_comment(post, follower_ids):
    return Comment(
        fake.sentence(nb_words=random.randint(15, 50)),
        random.choice(follower_ids),
        post.id
    )

def create_users(n=29):
    user = _create_webdev_user()
    users.append(user)
    db.session.add(user)
    db.session.commit()
    for _ in range(n):
        user = _create_user()
        users.append(user)
        db.session.add(user)
    db.session.commit()

def create_accounts_that_you_follow(users):
    for user in users:
        accounts_to_follow = []
        while len(accounts_to_follow) < 10:
            candidate_account = random.choice(users)
            if candidate_account != user and candidate_account not in accounts_to_follow:
                following = Following(user.id, candidate_account.id)
                db.session.add(following)


                # add to map:
                if user.id not in ppl_user_is_following_map:
                    ppl_user_is_following_map[user.id] = []
                ppl_user_is_following_map[user.id].append(candidate_account.id)
                
                accounts_to_follow.append(candidate_account)
    db.session.commit()
        
def create_posts(users):
    for user in users:
        for _ in range(random.randint(6, 12)):
            post = _create_post(user)
            posts.append(post)
            db.session.add(post)
    db.session.commit()

def create_stories(users):
    i = 0
    for user in users:
        if i % 3: # every third user has a story
            story = _create_story(user)
            db.session.add(story)
        i += 1
    db.session.commit()

def _get_people_who_follow(user_id):
    '''
    select bookmarks.user_id as owner_id, users.username as post_creator
    from bookmarks
    inner join posts on
        posts.id = bookmarks.post_id
    inner joing users on
    users.id = posts.user_id
    where bookmarks.user_id = 12;
    '''
    # print('-' * 100)
    # for key in ppl_user_is_following_map:
    #     print(key, ppl_user_is_following_map[key])
    # print('-' * 100)
    # return ppl_user_is_following_map[user_id].copy()
    user_ids_tuples = (
        db.session
            .query(Following.user_id)
            .filter(Following.following_id == user_id)
            .order_by(Following.user_id)
            .all()
    )
    # convert to a list of ints:
    return [id for (id,) in user_ids_tuples]

def create_post_likes(posts):
    for post in posts:
        auth_user_ids = _get_people_who_follow(post.user_id)
        _create_post_likes(post, auth_user_ids)
    db.session.commit()

def create_bookmarks(posts):
    for post in posts:
        '''
        Q: A user just posted an update. how do I find out who 
        follows that user?
        A: I query the "following" table for all the user_ids 
        where following_id = post.user_id        
        '''
        auth_user_ids = _get_people_who_follow(post.user_id)
        _create_post_bookmarks(post, auth_user_ids)
    db.session.commit()

def create_comments(posts):
    for post in posts:
        auth_user_ids = _get_people_who_follow(post.user_id)
        for _ in range(random.randint(0, 5)):
            comment = _create_comment(post, auth_user_ids)
            db.session.add(comment)
            comments.append(comment)
    db.session.commit()

def create_comment_likes(comments):
    for comment in comments:
        auth_user_ids = _get_people_who_follow(comment.user_id)
        for _ in range(random.randint(0, 3)):
            i = random.randint(0, len(auth_user_ids) - 1)
            user_id = auth_user_ids.pop(i)
            like = LikeComment(user_id, comment.id)
            db.session.add(like)
            if len(auth_user_ids) == 0:
                break
    db.session.commit()

# creates all of the tables if they don't exist:
with app.app_context():
    step = 1
    # uncomment if you want to drop all tables
    print('{0}. Dropping all tables...'.format(step))
    db.drop_all()
    step += 1 

    print('{0}. creating DB tables (if they don\'t already exist)...'.format(step))
    db.create_all()
    step += 1 

    print('{0}. creating 30 accounts (slow b/c of password hashing)...'.format(step))
    create_users(n=30)
    step += 1 

    print('{0}. assigning users some accounts to follow...'.format(step))
    create_accounts_that_you_follow(users)
    step += 1 

    print('{0}. creating fake posts...'.format(step))
    create_posts(users)
    step += 1 

    print('{0}. creating fake stories...'.format(step))
    create_stories(users)
    step += 1 

    print('{0}. creating fake post likes...'.format(step))
    create_post_likes(posts)
    step += 1 

    print('{0}. creating fake bookmarks...'.format(step))
    create_bookmarks(posts)
    step += 1 

    print('{0}. creating fake comments...'.format(step))
    create_comments(posts)
    step += 1

    print('{0}. creating fake comment likes...'.format(step))
    create_comment_likes(comments)
    step += 1  

    print('DONE!')