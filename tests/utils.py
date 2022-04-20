import os
from sqlalchemy import create_engine, inspect

from dotenv import load_dotenv
load_dotenv()

def modify_system_path():
    import os, sys, inspect
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0,parentdir) 

modify_system_path()

root_url = 'http://127.0.0.1:5000'
# root_url = 'https://photo-app-demo.herokuapp.com/'

connection_string = os.environ.get('DB_URL')
db = create_engine(connection_string, pool_size=10, max_overflow=0)

def _zip(columns, rows, single_object=True):
    results = []
    for row in rows:
        d = {}
        for i in range(len(columns)):
            d[columns[i]] = row[i]
        results.append(d)
    if len(results) == 1 and single_object:
        return results[0]
    else:
        return results


def get_user_12():
    with db.connect() as conn:
        inspector = inspect(db)
        columns = [c.get('name') for c in inspector.get_columns('users')]
        rows = conn.execute('SELECT * FROM users where id=12')
        conn.close()
        return _zip(columns, rows)

def get_user(user_id):
    with db.connect() as conn:
        inspector = inspect(db)
        columns = [c.get('name') for c in inspector.get_columns('users')]
        rows = conn.execute('SELECT * FROM users where id={0}'.format(user_id))
        conn.close()
        return _zip(columns, rows)


def get_unbookmarked_post_id_by_user(user_id):
    ids = get_authorized_user_ids(user_id)
    with db.connect() as conn:
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
                user_id=user_id,
                authorized_user_ids=', '.join([str(id) for id in ids])
            )
        rows = list(conn.execute(sql))
        conn.close()
        post_id = rows[0][0]
        return post_id

def get_unfollowed_user(user_id):
    with db.connect() as conn:
        inspector = inspect(db)
        sql = '''
            SELECT *
            FROM users
            WHERE id NOT IN (
                SELECT f.following_id 
                FROM following f
                WHERE f.user_id = {user_id} 
            )
            LIMIT 1
        '''.format(user_id=user_id)
        columns = [c.get('name') for c in inspector.get_columns('users')]
        rows = list(conn.execute(sql))
        conn.close()
        return _zip(columns, rows)

def get_unliked_post_id_by_user(user_id):
    ids = get_authorized_user_ids(user_id)
    with db.connect() as conn:
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
                user_id=user_id,
                authorized_user_ids=', '.join([str(id) for id in ids])
            )
        rows = list(conn.execute(sql))
        conn.close()
        post_id = rows[0][0]
        return post_id


def restore_post_by_id(post):
    with db.connect() as conn:
        sql = '''
            INSERT INTO posts(id, image_url, caption, alt_text, pub_date, user_id) 
            VALUES({id}, '{image_url}', '{caption}', '{alt_text}', now(), {user_id})
        '''.format(
            id=post.get('id'),
            image_url=post.get('image_url'),
            caption=post.get('caption'),
            alt_text=post.get('alt_text'),
            user_id=post.get('user_id')
        )
        conn.execute(sql)
        conn.close()

def restore_comment_by_id(comment):
    with db.connect() as conn:
        sql = '''
            INSERT INTO comments(id, post_id, user_id, text, pub_date) 
            VALUES({id}, {post_id}, {user_id}, '{text}', now())
        '''.format(
            id=comment.get('id'),
            post_id=comment.get('post_id'),
            user_id=comment.get('user_id'),
            text=comment.get('text')
        )
        conn.execute(sql)
        conn.close()

def restore_bookmark(bookmark):
    with db.connect() as conn:
        sql = '''
            INSERT INTO bookmarks(id, post_id, user_id, timestamp) 
            VALUES({id}, {post_id}, {user_id}, now())
        '''.format(
            id=bookmark.get('id'),
            post_id=bookmark.get('post_id'),
            user_id=bookmark.get('user_id'),
        )
        conn.execute(sql)
        conn.close()

def restore_liked_post(liked_post):
    with db.connect() as conn:
        sql = '''
            INSERT INTO likes_posts(id, post_id, user_id, timestamp) 
            VALUES({id}, {post_id}, {user_id}, now())
        '''.format(
            id=liked_post.get('id'),
            post_id=liked_post.get('post_id'),
            user_id=liked_post.get('user_id'),
        )
        conn.execute(sql)
        conn.close()

def restore_post(post_original_data):
    with db.connect() as conn:
        sql = '''
        UPDATE posts
        SET image_url = '{0}', caption = '{1}', alt_text = '{2}'
        WHERE id = {3}
        '''.format(
            post_original_data.get('image_url'),
            post_original_data.get('caption'),
            post_original_data.get('alt_text'),
            post_original_data.get('id')
        )
        conn.execute(sql)
        conn.close()

def restore_following(following_original):
    with db.connect() as conn:
        sql = '''
        INSERT INTO following(id, user_id, following_id) 
            VALUES({id}, {user_id}, {following_id})
        '''.format(
            id=following_original.get('id'),
            user_id=following_original.get('user_id'),
            following_id=following_original.get('following_id')
        )
        conn.execute(sql)
        conn.close()

def get_following_ids(user_id):
    with db.connect() as conn:
        inspector = inspect(db)

        # first get list of authorized usernames:
        sql = '''
            SELECT *
            FROM following 
            WHERE following.user_id = {0} 
            ORDER BY following.following_id
        '''.format(user_id)
        columns = [c.get('name') for c in inspector.get_columns('following')]
        rows = conn.execute(sql)
        conn.close()
        records = _zip(columns, rows)
        return [rec.get('following_id') for rec in records]

def get_follower_ids(user_id):
    with db.connect() as conn:
        inspector = inspect(db)

        # first get list of authorized usernames:
        sql = '''
            SELECT *
            FROM following 
            WHERE following.following_id = {0} 
            ORDER BY following.user_id
        '''.format(user_id)
        columns = [c.get('name') for c in inspector.get_columns('following')]
        rows = conn.execute(sql)
        conn.close()
        records = _zip(columns, rows)
        return [rec.get('user_id') for rec in records]

def get_authorized_user_ids(user_id):
    ids = get_following_ids(user_id)
    ids.append(user_id)
    return ids

def get_post_that_user_cannot_access(user_id):
    with db.connect() as conn:
        inspector = inspect(db)
        ids = get_authorized_user_ids(user_id)

        # then query for a post that was NOT created by one of these users:
        sql = '''
            SELECT posts.id, posts.image_url, posts.caption, posts.alt_text, 
                posts.pub_date, posts.user_id
            FROM posts 
            LEFT OUTER JOIN users AS users_1 ON 
                users_1.id = posts.user_id 
            WHERE (posts.user_id NOT IN ({0})) 
            LIMIT 1
        '''.format(', '.join([str(id) for id in ids]))
        columns = [c.get('name') for c in inspector.get_columns('posts')]
        rows = conn.execute(sql)
        conn.close()
        object = _zip(columns, rows)
        return object


def get_x_that_user_cannot_delete(table_name, user_id):
    with db.connect() as conn:
        inspector = inspect(db)
        # then query for a post that was NOT created by one of these users:
        sql = 'SELECT * FROM {0} where user_id != {1} LIMIT 1'.format(table_name, user_id)
        columns = [c.get('name') for c in inspector.get_columns(table_name)]
        rows = conn.execute(sql)
        conn.close()
        object = _zip(columns, rows)
        return object


def get_comment_that_user_cannot_delete(user_id):
    return get_x_that_user_cannot_delete('comments', user_id)


def get_bookmark_that_user_cannot_delete(user_id):
    return get_x_that_user_cannot_delete('bookmarks', user_id)


def get_following_that_user_cannot_delete(user_id):
    return get_x_that_user_cannot_delete('following', user_id)


def get_liked_post_that_user_cannot_delete(user_id):
    return get_x_that_user_cannot_delete('likes_posts', user_id)


def get_stories_by_user(user_id):
    with db.connect() as conn:
        ids = get_authorized_user_ids(user_id)
        sql = '''
            SELECT stories.id
            FROM stories 
            LEFT OUTER JOIN users AS users_1 ON 
                users_1.id = stories.user_id 
            WHERE stories.user_id IN ({user_ids})
        '''.format(user_ids=', '.join([str(id) for id in ids]))
        rows = conn.execute(sql)
        conn.close()
        story_ids = [row[0] for row in rows]
        return story_ids

def get_unrelated_users(user_id):
    with db.connect() as conn:
        ids = get_authorized_user_ids(user_id)

        # then query for a post that was NOT created by one of these users:
        sql = '''
            SELECT id FROM users where id NOT IN ({0})
        '''.format(', '.join([str(id) for id in ids]))
        rows = conn.execute(sql)
        conn.close()
        return [row[0] for row in rows]

def delete_x_by_id(table_name, id):
    with db.connect() as conn:
        sql = 'DELETE FROM {0} where id={1}'.format(table_name, id)
        conn.execute(sql)
        conn.close()


def delete_post_by_id(id):
    delete_x_by_id('posts', id)


def delete_comment_by_id(id):
    delete_x_by_id('comments', id)


def delete_bookmark_by_id(id):
    delete_x_by_id('bookmarks', id)


def delete_like_by_id(id):
    delete_x_by_id('likes_posts', id)


def delete_following_by_id(id):
    delete_x_by_id('following', id)


def get_bookmark_ids(user_id):
    with db.connect() as conn:
        # then query for a post that was NOT created by one of these users:
        sql = 'SELECT id FROM bookmarks where user_id = ({0})'.format(user_id)
        rows = conn.execute(sql)
        conn.close()
        return [row[0] for row in rows]


def get_x_by_user(table_name, user_id):
    with db.connect() as conn:
        inspector = inspect(db)
        # then query for a post that was NOT created by one of these users:
        sql = 'SELECT * FROM {0} where user_id = ({1}) LIMIT 1'.format(table_name, user_id)
        rows = conn.execute(sql)
        columns = [c.get('name') for c in inspector.get_columns(table_name)]
        conn.close()
        object = _zip(columns, rows)
        return object


def get_post_by_user(user_id):
    return get_x_by_user('posts', user_id)


def get_bookmarked_post_by_user(user_id):
    return get_x_by_user('bookmarks', user_id)


def get_liked_post_by_user(user_id):
    return get_x_by_user('likes_posts', user_id)


def get_comment_by_user(user_id):
    return get_x_by_user('comments', user_id)


def get_bookmark_by_user(user_id):
    return get_x_by_user('bookmarks', user_id)


def get_following_by_user(user_id):
    return get_x_by_user('following', user_id)


def get_x_by_id(table_name, id):
    with db.connect() as conn:
        inspector = inspect(db)
        columns = [c.get('name') for c in inspector.get_columns(table_name)]
        sql = 'SELECT * FROM {0} where id={1}'.format(table_name, id)
        rows = conn.execute(sql)
        return _zip(columns, rows)


def get_post_by_id(id):
    return get_x_by_id('posts', id)


def get_comment_by_id(id):
    return get_x_by_id('comments', id)


def get_bookmark_by_id(id):
    return get_x_by_id('bookmarks', id)


def get_liked_post_by_id(id):
    return get_x_by_id('likes_posts', id)


def get_following_by_id(id):
    return get_x_by_id('following', id)
        