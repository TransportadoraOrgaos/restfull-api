from db import db

class ReportModel(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(80))
    latitude = db.Column(db.Integer)
    longitude = db.Column(db.Integer)
    temperature = db.Column(db.Integer)
    is_locked = db.Column(db.Boolean)

    transport_id = db.Column(db.Integer, db.ForeignKey('transports.id'))
    transport = db.relationship('TransportModel')

    def __init__(self, date, latitude, longitude, temperature, transport_id, is_locked):
        self.date = date
        self.latitude = latitude
        self.longitude = longitude
        self.temperature = temperature
        self.transport_id = transport_id
        self.is_locked = is_locked

    def json(self):
        return {
            'date': self.date,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'temperature': self.temperature,
            'transport_id': self.transport_id,
            'is_locked': self.is_locked
        }

    @classmethod
    def find_by_transport_id(cls, transport_id):
        return cls.query.filter_by(transport_id=transport_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()