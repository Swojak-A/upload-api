import datetime
from app import db


class Upload(db.Model):

    __tablename__ = 'uploads'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    date_uploaded = db.Column(db.DateTime, nullable=False)

    def __init__(self, **kwargs):
        super(Upload, self).__init__(**kwargs)
        # do custom initialization here
        self.date_uploaded = datetime.datetime.utcnow()