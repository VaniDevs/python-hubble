import falcon
import json
import boto3
import uuid
import base64
import os

from hubble import models
from hubble.models import Event

access_key = os.environ['S3_KEY']
secret_key = os.environ['S3_SECRET']
s3_region_name = os.environ.get('S3_REGION', 'ca-central-1')
bucket_name = os.environ.get('S3_BUCKET', 'vanhacks2018')

s3 = boto3.resource('s3', region_name=s3_region_name, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
client = boto3.client('s3', region_name=s3_region_name, aws_access_key_id=access_key, aws_secret_access_key=secret_key)

def uploadImageToS3(image):
    key = str(uuid.uuid4())

    decoded_image = base64.b64decode(image)

    print("saving key " + key)
    client.put_object(Bucket=bucket_name, Key=key, Body=decoded_image)
    print("Getting S3 object " + key)
    response = client.get_object(Bucket=bucket_name, Key=key)
    print(response)
    image_url = "http://s3-" + s3_region_name + ".amazonaws.com/" + bucket_name + "/" + key  # almost 100% sure this is not right yet
    print(image_url)
    return image_url

def handleImagePost(req, resp):

    (lat, lng) = req.media['location']['geometry']['coordinates']

    image_url = uploadImageToS3(req.body.image_data)

    event = Event(image_url, lat, lng, req.comments)
    event.save()

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
        handleImagePost(req, resp)

