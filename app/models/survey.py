from datetime import datetime, timedelta
from app import db

class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    age = db.Column(db.Integer())
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    gender = db.Column(db.Integer)
    side = db.Column(db.Integer)
    falls = db.Column(db.Integer)
    medicines = db.Column(db.Boolean)
    hearing_vision = db.Column(db.Boolean)
    stool_urine = db.Column(db.Boolean)
    other_diseases = db.Column(db.Boolean)
    walking_assist = db.Column(db.Boolean)
    home_risk = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Survey {}>'.format(self.id)

    def to_dict(self, string_dates=False):
        data = {
            'id' : self.id,
            'user_id' : self.user_id,
            'age' : self.age,
            'height' : self.height,
            'weight' : self.weight,
            'gender' : self.gender,
            'side' : self.side,
            'falls' : self.falls,
            'medicines' : self.medicines,
            'hearing_vision' : self.hearing_vision,
            'stool_urine' : self.stool_urine,
            'other_diseases' : self.other_diseases,
            'walking_assist' : self.walking_assist,
            'home_risk' : self.home_risk
        }

        if string_dates and self.timestamp is not None:
            data['timestamp'] = self.timestamp.isoformat()
        else:
            data['timestamp'] = self.timestamp

    def from_dict(self, data):
        for field in ['user_id', 'age', 'height', 'weight', 'gender', 'side',
                'falls', 'medicines', 'hearing_vision', 'stool_urine',
                'other_diseases', 'walking_assist', 'home_risk']:
            if field in data:
                setattr(self, field, data[field])
