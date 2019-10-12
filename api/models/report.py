from api.core import Mixin
from .base import db


class Report(Mixin, db.Model):
    """Reports Table."""

    __tablename__ = "reports"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    device_id = db.Column(db.Integer, unique=True)
    datetime = db.Column(db.Integer)
    latency = db.Column(db.Float)
    download = db.Column(db.Float)
    upload = db.Column(db.Float)

    def __init__(self, device_id, datetime, latency, download, upload):
        self.device_id = device_id,
        self.datetime = datetime,
        self.latency = latency,
        self.download = download,
        self.upload = upload

    def json(self):
        return {
            'device_id': self.device_id,
            'datetime': self.datetime,
            'latency': self.latency,
            'download': self.download,
            'upload': self.upload
        }

    @classmethod
    def find_by_device_id(cls, device_id):
        return cls.query.filter_by(device_id=device_id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"<Report {self.device_id}>"  # noqa: E999
