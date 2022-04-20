from datetime import datetime
from . import db

class Story(db.Model):
    __tablename__ = 'stories'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'),
        nullable=False)

    # read-only:
    user = db.relationship('User', backref="stories", lazy=False)

    def __init__(self, text:str, user_id:int, pub_date:datetime=None):
        self.text = text
        self.user_id = int(user_id)
        self.pub_date = pub_date
    
    def __repr__(self):
        return '<Story %r>' % self.id

    def to_dict(self): 
        return {
            'id': self.id,
            'text': self.text,
            'user': self.user.to_dict()
        }
