from api import db


class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    base_url = db.Column(db.String(256))
    requests = db.relationship("Request", backref="collection", lazy=True)

    def __repr__(self):
        return f"<Collection {self.name}>"

    @classmethod
    def __get_column_names__(cls):
        return [column.name for column in cls.__table__.columns]

    def to_dict(self):
        data = {"id": self.id, "name": self.name, "base_url;": self.base_url}
        return data

    def from_dict(self, data):
        for field in self.__get_column_names__():
            if field in data:
                setattr(self, field, data[field])

    @staticmethod
    def to_collection_dict(query):
        collections = query
        data = {"collections": [c.to_dict() for c in collections]}

        return data


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(245))
    url = db.Column(db.String(256), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    parameters = db.Column(db.JSON)
    collection_id = db.Column(db.Integer, db.ForeignKey("collection.id"), nullable=False)
    monitor_id = db.Column(db.Integer, db.ForeignKey("monitor.id"))

    def __repr__(self):
        return f"<Request {self.url}>"

    @classmethod
    def __get_column_names__(cls):
        return [column.name for column in cls.__table__.columns]

    def to_dict(self):
        data = {
            "name": self.name,
            "endpoint": self.url,
            "method": self.method,
            "collection_id": self.collection_id,
            "collection_name": Collection.query.get(self.collection_id).name,
            "parameters": self.parameters,
        }
        return data

    def from_dict(self, data):
        for field in self.__get_column_names__():
            if field in data:
                setattr(self, field, data[field])

    @staticmethod
    def to_requests_dict(query):
        requests = query
        data = {"requests": [r.to_dict() for r in requests]}
        return data


class Monitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    requests = db.relationship("Request", backref="monitor", lazy=True)

    def __repr__(self):
        return f"<Monitor {self.name}>"
