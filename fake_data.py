import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

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

def format_display_time(the_date):
    diff = datetime.now() - the_date
    days = diff.days
    hours = diff.seconds // 3600
    if days == 0:
        if hours < 0:
            return 'Just now'
        elif hours == 1:
            return '1 hour ago'
        else:
            return '{0} hours ago'.format(hours)
    elif days == 1:
        return '1 day ago'
    else:
        return '{0} days ago'.format(days)

def generate_user():
    '''
    Generates a fake user, which is returned as a dictionary.
    '''
    profile = fake.simple_profile()
    tokens = profile['name'].split(' ')
    first_name = tokens.pop(0)
    last_name = ' '.join(tokens)
    username = profile['username']
    email = profile['mail']
    image_id = random.randint(0, 1000)
    image_url = generate_image(id=image_id, width=300, height=200)
    profile_url = generate_image(id=image_id, width=50, height=50)
    thumb_url = generate_image(id=image_id, width=30, height=30)

    # return dictionary representation of the user:
    return {
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'image_url': image_url,
        'profile_url': profile_url,
        'thumb_url': thumb_url 
    }


def generate_posts(n=10, width=300, height=200):
    '''
    Generates fake post data for prototyping:
        * n (int): number of posts you want to generate
        * width (int): width of the pic
        * height (int): height of the pic
    Returns a list of n dictionaries where each dictionary 
    represents a post and corresponding comments.
    '''
    posts = []
    for _ in range(n):
        # random post time:
        time_of_post = datetime.now() - timedelta(hours=random.randint(1, 40))
        post = {
            'title': fake.sentence(nb_words=random.randint(10, 40)),
            'image_url': generate_image(width=width, height=height),
            'likes': random.randint(1, 100),
            'user': generate_user(),
            'time_posted': time_of_post.isoformat(),
            'display_time': format_display_time(time_of_post),
            'comments': []
        }
        
        # each post can have up to 8 comments:
        for _ in range(0, random.randint(0, 8)):
            post['comments'].append({
                'text': fake.sentence(nb_words=10),
                'user': generate_user()
            })
        posts.append(post)
    return posts


def generate_stories(n:int=5):
    '''
    Generates fake story data for prototyping:
        * n (int): number of stories you want to generate
    Returns a list of n dictionaries where each dictionary 
    represents a story.
    '''
    stories = []
    for _ in range(n):
        stories.append({
            'title': fake.sentence(nb_words=10),
            'user': generate_user()
        })
    return stories


def generate_suggestions(n=8):
    '''
    Generates fake account data for prototyping:
        * n (int): number of posts you want to generate
    Returns a list of n dictionaries where each dictionary 
    represents a user account.
    '''
    suggestions = []
    for _ in range(n):
        suggestions.append(generate_user())
    return suggestions
