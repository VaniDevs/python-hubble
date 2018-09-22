import json


class Event:
    def __init__(self, img_data, lat, long, comments=None):
        self.img_data = img_data
        self.lat = lat
        self.long = long
        self.comments = comments

    def save(self):
        # TODO: wire up to db
        _EVENTS.append(self)

    @staticmethod
    def all():
        # TODO: wire up to db
        return _EVENTS 


def _generate_debug_data():
    import random, base64

    with open('data/meme.jpg', 'rb') as test_img:
        img_data = base64.b64encode(test_img.read())

    events = []

    for _ in range(100):
        lat = random.uniform(-90, 90)
        long = random.uniform(-180, 180)

        events.append(
            Event(
                random.uniform(-90, 90),
                random.uniform(-90, 90),
                'someting bad happened'
            )
        )

    return events

_EVENTS = _generate_debug_data()
