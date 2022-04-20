from datetime import datetime
from . import db

class LikePost(db.Model):
    __tablename__ = 'likes_posts'

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

    def __init__(self, user_id:int, post_id:int):
        self.user_id = int(user_id)
        self.post_id = int(post_id)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'post_id': self.post_id
        }

    def __repr__(self):
        return '<Like Post %r>' % self.id
