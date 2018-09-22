import falcon
import json
import boto3
import time
import uuid

from hubble.models import Event

s3_region_name = 'ca-central-1'

s3 = boto3.resource('s3', region_name=s3_region_name)

bucket_name = "vanhacks2018"
key = str(uuid.uuid4())
# s3.put_object(Bucket=bucketName, Key=key, Body=b'foobar')


class HelloWorld:
    def on_get(self, req, resp, key=None):
        if key is None:
            resp.media = json.dumps({'hello': 'world'})
        else:
            resp.media = json.dumps({'hello': key})


class SendUpdate:
    def on_post(self, req, resp):
        print("saving key " + key)
        s3.put_object(Bucket=bucket_name, Key=key, Body=b'foobar')
        print("Getting S3 object " + key)
        response = s3.get_object(Bucket=bucket_name, Key=key)
        image_url = "http://s3-" + s3_region_name + ".amazonaws.com/" + bucket_name + "/" + key
        event = Event(image_url, req.lat, req.long, req.comments)
        event.save()
