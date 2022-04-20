from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def output_raw_sql(query):
    '''
    Sample usage:
    output_raw_sql(Post.query.limit(10))
    output_raw_sql(
        db.session
            .query(Following.following_id)
            .filter(Following.user_id == 5)
            .order_by(Following.following_id)
        )
    '''
    from sqlalchemy.dialects import postgresql
    print(str(query.statement.compile(dialect=postgresql.dialect())))


from .bookmark import Bookmark
from .comment import Comment
from .following import Following
from .like_comment import LikeComment
from .like_post import LikePost
from .post import Post
from .story import Story
from .user import User
from .api_structure import ApiNavigator
