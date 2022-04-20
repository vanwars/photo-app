from datetime import datetime
from . import db

class Bookmark(db.Model):
    __tablename__ = 'bookmarks'

    __table_args__ = (
        db.UniqueConstraint('user_id', 'post_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'),
        nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='cascade'),
        nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    # read-only property for referencing User properties
    post = db.relationship('Post', backref="bookmarks", lazy=False)

    def __init__(self, user_id:int, post_id:int):
        self.user_id = int(user_id)
        self.post_id = int(post_id)

    def to_dict(self):
        return {
            'id': self.id,
            'post': self.post.to_dict(include_comments=False)
        }

    def __repr__(self):
        return '<Bookmark %r>' % self.id       
