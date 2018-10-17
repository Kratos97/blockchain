from app import db


class Commodity(db.Model):
    # 表的名字:,或者derived from the class name converted to lowercase and with “CamelCase” converted to “camel_case
    __tablename__ = 'bc_commodity'
    #colums
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(80), unique=True, nullable=True,default='')
    event_time = db.Column(db.DateTime, nullable=True)
    location = db.Column(db.String(80), unique=False, nullable=True,default='')
    person = db.Column(db.String(20), unique=False, nullable=True)
    tel = db.Column(db.String(80), unique=False, nullable=True)
    desc = db.Column(db.String(200), unique=False, nullable=True)
    random_num = db.Column(db.Integer, unique=False, nullable=True)
    current_hash = db.Column(db.String(200), unique=False, nullable=True)
    pre_hash = db.Column(db.String(200), unique=False, nullable=True)
    status = db.Column(db.String(5), unique=False, nullable=True)
    chain_index = db.Column(db.Integer, unique=False, nullable=True)


    def __repr__(self):
        return '<Commodity %r>' % self.event_name








