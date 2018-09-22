import falcon
import json
import boto3
import time

from hubble.models import Event

s3 = boto3.resource('s3', region_name='ca-central-1')

bucketName = "vanhacks2018"
key = "uploadFileName"
outputName = int(round(time.time() * 1000))
# s3.put_object(Bucket=bucketName, Key=key, Body=b'foobar')

class HelloWorld:
    def on_get(self, req, resp, key=None):
        if key is None:
            resp.media = json.dumps({'hello': 'world'})
        else:
            resp.media = json.dumps({'hello': key})

class SendUpdate:
    def on_post(self, req, resp):
        s3.put_object(Bucket=bucketName, Key=key, Body=b'foobar')
        event = Event(req.img_data, req.lat, req.long, req.comments)
        event.save()