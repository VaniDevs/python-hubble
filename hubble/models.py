import json
import sqlalchemy
from sqlalchemy.dialects import postgresql


engine = None
metadata = sqlalchemy.MetaData()


def initdb(uri):
    global engine
    engine = sqlalchemy.create_engine(uri)


class Event:
    def __init__(self, url, lat, long, comments=None):
        self.url = url
        self.lattitude = lat
        self.longitude = long
        self.comments = comments

    def save(self):
        # TODO: wire up to db
        _EVENTS.append(self)

    @staticmethod
    def all():
        # TODO: wire up to db
        return _EVENTS 


_events = sqlalchemy.Table(
    'events',
    metadata,
    sqlalchemy.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
)


def _generate_debug_data():
    import random, base64

    events = []

    for _ in range(100):
        lat = random.uniform(-90, 90)
        long = random.uniform(-180, 180)

        events.append(
            Event(
                'https://i.kym-cdn.com/photos/images/newsfeed/001/217/729/f9a.jpg',
                random.uniform(-90, 90),
                random.uniform(-90, 90),
                'something bad happened'
            )
        )

    return events

_EVENTS = _generate_debug_data()
