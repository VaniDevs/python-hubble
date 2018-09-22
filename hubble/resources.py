import falcon
import json

from hubble import models



class Event:
    def on_get(self, req, resp):
        filters = req.params
        events = models.Event.all(
            offset=filters.get('offset'),
            limit=filters.get('limit')
        )
        resp.media = [
            {
                'id': str(ev.id),
                'image_url': ev.image_url,
                'comments': ev.comments,
                'location': {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [ev.longitude, ev.lattitude],
                    },
                    "properties": {
                        "name": ev.location_name,
                    }
                },
                'created': ev.created,
            }
            for ev in events
        ]
