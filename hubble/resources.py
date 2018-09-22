import falcon
import json
import boto3
import time
import uuid

from hubble.models import Event
from hubble import models


s3_region_name = 'ca-central-1'

s3 = boto3.resource('s3', region_name=s3_region_name)

bucket_name = "vanhacks2018"
key = str(uuid.uuid4())
# s3.put_object(Bucket=bucketName, Key=key, Body=b'foobar')



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


class SendUpdate:
    def on_post(self, req, resp):

        lat = ""
        long = ""

        with open(req.geoJson) as geoJson:
            data = json.load(geoJson)
        for feature in data['features']:
            lat = feature['geometry']['coordinates'][0]
            long = feature['geometry']['coordinates'][1]

        print("saving key " + key)
        s3.put_object(Bucket=bucket_name, Key=key, Body=b'foobar')
        print("Getting S3 object " + key)
        response = s3.get_object(Bucket=bucket_name, Key=key)
        image_url = "http://s3-" + s3_region_name + ".amazonaws.com/" + bucket_name + "/" + key
        event = Event(image_url, lat, long, req.comments)
        event.save()
