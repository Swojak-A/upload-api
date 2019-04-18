import datetime
from app import db


class Upload(db.Model):

    __tablename__ = 'uploads'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    date_uploaded = db.Column(db.DateTime, nullable=False)

    def __init__(self, filename, url):
        self.filename = filename
        self.url = url
        self.date_uploaded = datetime.datetime.now()