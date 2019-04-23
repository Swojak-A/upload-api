from datetime import datetime
from app import db


class Upload(db.Model):

    __tablename__ = 'uploads'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    original_filename = db.Column(db.String, nullable=False) # FileStorage werkzeug object has problems being pickled
    file = db.Column(db.LargeBinary, nullable=False) # so we save orig name as string and file itself as BLOB
    date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
