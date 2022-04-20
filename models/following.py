from . import db


class Following(db.Model):

    __tablename__ = 'following'

    __table_args__ = (
        db.UniqueConstraint('user_id', 'following_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'),
        nullable=False)
    following_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'),
        nullable=False)
    follower = db.relationship('User', backref="follower", lazy=False, foreign_keys='Following.user_id')
    following = db.relationship('User', backref="following", lazy=False, foreign_keys='Following.following_id')

    db.UniqueConstraint('user_id', 'following_id', name='following_unique')

    def __init__(self, user_id:int, following_id:int):
        self.user_id = int(user_id)
        self.following_id = int(following_id)

    def to_dict_following(self): 
        return {
            'id': self.id,
            'following': self.following.to_dict()
        }

    def to_dict_follower(self):
        return {
            'id': self.id,
            'follower': self.follower.to_dict()
        }
