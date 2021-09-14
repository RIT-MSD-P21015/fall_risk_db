from datetime import datetime, timedelta
from app import db
from app.models.sample import Sample

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_type = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    n = db.Column(db.Integer)
    period = db.Column(db.Float)

    def __repr__(self):
        return '<Test {}>'.format(self.id)

    def to_dict(self, include_samples=False, string_dates=False):
        data = {
            'id' : self.id,
            'test_type' : self.test_type,
            'user_id' : self.user_id,
            'n' : self.n,
            'period' : self.period,
        }

        if not string_dates:
            data['timestamp'] = self.timestamp
        else:
            data['timestamp'] = self.timestamp.isoformat()

        if include_samples == False:
            return data

        samples = Sample.query.filter_by(test_id=self.id).order_by(Sample.index).all()

        data['samples'] = []
        for sample in samples:
            data['samples'].append(sample.to_dict())

        return data

    def from_dict(self, data):
        for field in ['test_type', 'user_id', 'n', 'period']:
            if field in data:
                setattr(self, field, data[field])
