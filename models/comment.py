from datetime import datetime
from . import db

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'),
        nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='cascade'),
        nullable=False)

    # read-only:
    user = db.relationship('User', backref="comments", lazy=False)

    def __init__(self, text:str, user_id:int, post_id:int):
        self.text = text
        self.user_id = int(user_id)
        self.post_id = int(post_id)
    
    def __repr__(self):
        return '<Comment %r>' % self.id

    def to_dict(self): 
        return {
            'id': self.id,
            'text': self.text,
            'post_id': self.post_id,
            'user': self.user.to_dict()
        }
