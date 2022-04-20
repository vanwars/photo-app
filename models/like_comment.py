from datetime import datetime
from . import db

class LikeComment(db.Model):
    __tablename__ = 'likes_comments'

    __table_args__ = (
        db.UniqueConstraint('user_id', 'comment_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'),
        nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id', ondelete='cascade'),
        nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    def __repr__(self):
        return '<Like Comment %r>' % self.id

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'comment_id': self.comment_id
        }

    def __init__(self, user_id:int, comment_id:int):
        self.user_id = int(user_id)
        self.comment_id = int(comment_id)
 
