import json
import time
import uuid

import sqlalchemy
from sqlalchemy.dialects import postgresql


_engine = None
_conn = None
_metadata = sqlalchemy.MetaData()


def initdb(uri):
    global _engine, _conn
    _engine = sqlalchemy.create_engine(uri)
    _conn = _engine.connect()


def createdb():
    _metadata.create_all(_engine)


class Model:
    def save(self, statement):
        _conn.execute(statement)


class Event(Model):
    _table = sqlalchemy.Table(
        'events',
        _metadata,
        sqlalchemy.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sqlalchemy.Column('url', sqlalchemy.String),
        sqlalchemy.Column('lattitude', sqlalchemy.Float),
        sqlalchemy.Column('longitude', sqlalchemy.Float),
        sqlalchemy.Column('comments', sqlalchemy.String),
        sqlalchemy.Column('created', sqlalchemy.Integer),
    )

    def __init__(self, url, lattitude, longitude, comments=None, id=None,
                 created=None):
        self.url = url
        self.lattitude = lattitude
        self.longitude = longitude
        self.comments = comments
        self.created = created or time.time()


    def save(self):
        id = uuid.uuid4()
        ev = Event._table.insert().values(
            id=id,
            url=self.url,
            lattitude=self.lattitude,
            longitude=self.longitude,
            comments=self.comments
        )
        self.id = id
        super().save(ev)

    @staticmethod
    def all(offset=None, limit=None):
        query = Event._table.select().order_by(Event._table.c.created.desc())
        if offset:
            query = query.offset(offset)

        if limit:
            query = query.limit(offset)

        cur = _conn.execute(query)
        events = [ev for ev in cur]
        cols = cur.keys()
        return [
            Event(**{cols[idx]: val for idx, val in enumerate(ev)})
            for ev in events
        ]
