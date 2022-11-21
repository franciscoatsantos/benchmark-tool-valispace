from api import db


class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    base_url = db.Column(db.String(256))
    requests = db.relationship("Request", backref='collection', lazy=True)

    def __repr__(self):
        return f'<User {self.name}>'

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'base_url;': self.base_url
        }
        return data

    @staticmethod
    def to_collection_dict(query):
        collections = query
        data = {
            "collections": [c.to_dict for c in collections]
        }

        return data


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(256))
    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'), nullable=False)

    def __repr__(self):
        return f'<Request {self.url}>'

    def to_dict(self):
        data = {
            "endpoint": self.url,
            "collection_id": self.collection_id,
            "collection_name": Collection.query.get(self.collection_id).name
        }
        return data
    @staticmethod
    def to_requests_dict(query):
        requests = query
