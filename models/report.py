from db import db

class ReportModel(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(80))
    latitude = db.Column(db.Integer)
    longitude = db.Column(db.Integer)
    temperature = db.Column(db.Integer)
    is_locked = db.Column(db.Integer)
    enable = db.Column(db.Integer)
    transport_id = db.Column(db.Integer, db.ForeignKey('transports.id'))
    
    transport = db.relationship('TransportModel')

    def __init__(self, date, latitude, longitude, temperature,  is_locked, transport_id, enable):
        self.date = date
        self.latitude = latitude
        self.longitude = longitude
        self.temperature = temperature
        self.is_locked = is_locked
        self.transport_id = transport_id
        self.enable = enable

    def json(self):
        return {
            'date': self.date,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'temperature': self.temperature,
            'is_locked': self.is_locked,
            'transport_id': self.transport_id,
            'enable': self.enable
        }

    @classmethod
    def find_by_transport_id(cls, transport_id):
        return cls.query.filter_by(transport_id=transport_id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()