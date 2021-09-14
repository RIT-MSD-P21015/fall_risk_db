from datetime import datetime, timedelta
from app import db

class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), index=True)
    gyrox = db.Column(db.Float)
    gyroy = db.Column(db.Float)
    gyroz = db.Column(db.Float)
    accelx = db.Column(db.Float)
    accely = db.Column(db.Float)
    accelz = db.Column(db.Float)
    index = db.Column(db.Integer)

    def __repr__(self):
        return '<Sample {}>'.format(self.id)

    def to_dict(self):
        data = {
            'test_id' : self.test_id,
            'gyrox' : self.gyrox,
            'gyroy' : self.gyroy,
            'gyroz' : self.gyroz,
            'accelx' : self.accelx,
            'accely' : self.accely,
            'accelz' : self.accelz,
            'index' : self.index
        }

        return data

    def from_dict(self, data, test_id=None):
        for field in ['gyrox', 'gyroy', 'gyroz', 'accelx', 'accely', 'accelz', 'index']:
            if field in data:
                setattr(self, field, data[field])
        if test_id is not None:
            self.test_id = test_id
