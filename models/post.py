from datetime import datetime
from . import db
from .utils import get_display_time

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.Text, nullable=True)
    alt_text = db.Column(db.Text, nullable=True)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'),
        nullable=False)

    # read-only property for referencing User properties
    user = db.relationship('User', backref="posts", lazy=False)
    comments = db.relationship('Comment', cascade="all,delete-orphan", lazy='select', 
        order_by='Comment.pub_date', backref=db.backref('posts', lazy='joined'))
    likes = db.relationship('LikePost', cascade="all,delete-orphan", lazy='select',
        order_by='LikePost.timestamp', backref=db.backref('posts', lazy='joined'))

    def __init__(self, image_url, user_id, caption=None, alt_text=None, pub_date=None):
        self.image_url = image_url
        self.user_id = user_id
        self.caption = caption
        self.alt_text = alt_text
        self.pub_date = pub_date

    def __repr__(self):
        return '<Post={0} by User={1}>'.format(self.id, self.user_id)


    def to_dict(self, include_comments:bool=True, user=None): 
        d = {
            'id': self.id,
            'image_url': self.image_url,
            'user': self.user.to_dict(),
            'caption': self.caption, 
            'alt_text': self.alt_text,
            'display_time': get_display_time(self.pub_date),
            'likes': [like.to_dict() for like in self.likes]
        }
        if include_comments:
            d['comments'] = [
                comment.to_dict() for comment in self.comments
            ]

        # some convenience properties of the post:
        if user:
            def filter_function(item):
                return item.user_id == user.id

            user_like_id_list = [like.id for like in filter(filter_function, self.likes)]
            user_bookmark_id_list = [bookmark.id for bookmark in filter(filter_function, self.bookmarks)]
            print(user_like_id_list)
            if len(user_like_id_list) == 1:
                d['current_user_like_id'] = user_like_id_list[0]
            if len(user_bookmark_id_list) == 1:
                d['current_user_bookmark_id'] = user_bookmark_id_list[0]
        
        return d
 