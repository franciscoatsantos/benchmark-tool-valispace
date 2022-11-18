from api import db


class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    base_url = db.Column(db.String(256))
    requests = db.relationship("Request", backref='collection', lazy=True)


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(256))
    collection_id = db.Column(db.Integer, db.ForeignKey('person_id'), nullable=False)
