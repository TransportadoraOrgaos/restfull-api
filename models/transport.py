from db import db

class TransportModel(db.Model):
    __tablename__ = 'transports'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    organ = db.Column(db.String(80))
    responsible = db.Column(db.String(80))
    box_id = db.Column(db.Integer, db.ForeignKey('boxes.id'))
    
    box = db.relationship('BoxModel')
    reports = db.relationship('ReportModel', lazy='dynamic')

    def __init__(self, organ, responsible, box_id):
        self.organ = organ
        self.responsible = responsible
        self.box_id = box_id

    def json(self):
        return {'id': self.id, 'organ': self.organ, 'responsible': self.responsible, 'box_id': self.box_id, 'reports': [report.json() for report in self.reports.all()]}

    @classmethod
    def find_by_transport_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()