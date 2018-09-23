import falcon
import json
import boto3
import uuid
import base64
import os
import io
import enum

from PIL import Image

from hubble import models, client_config, cors, tasks
from hubble.models import Event


class ClientConfig:
    def on_get(self, req, resp):
        resp.media = client_config.settings


MAX_WIDTH, MAX_HEIGHT = (500, 500)
class Axis(enum.IntEnum):
    X = 0
    Y = 1


def handleImagePost(data):
    buffer = io.BytesIO(base64.b64decode(data['image_data']))

    img = Image.open(buffer)
    out_buffer = io.BytesIO()

    if img.width > MAX_WIDTH or img.height > MAX_HEIGHT:
        scale_axis = Axis.Y if img.height > img.width else Axis.X
        if scale_axis == Axis.Y:
            img = img.resize(
                (int(img.width * (MAX_HEIGHT / img.height)), int(MAX_HEIGHT))
            )
        else:
            img = img.resize(
                (int(MAX_WIDTH), int(img.height * (MAX_WIDTH / img.width)))
            )
    
    img.save(out_buffer, 'JPEG')
    (lat, lng) = data['location']
    location_name = data['name']

    tasks.process_event.apply_async(
        args=(
            location_name,
            base64.b64encode(out_buffer.getvalue()).decode('utf8'),
            lat, lng, data['comment']
        )
    )


class Event:
    @cors.allow
    def on_get(self, req, resp):
        events = models.Event.all(
            offset=req.params.get('offset'),
            limit=req.params.get('limit'),
            area=req.params.get('area'),
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

    def on_post(self, req, resp):
        data = req.media
        resp.media = handleImagePost(data)
