import celery
import logging
import uuid
import boto3
import requests
from os import environ

from hubble import models


app = celery.Celery(__name__, broker=environ['REDIS_URL'])

access_key = environ['S3_KEY']
secret_key = environ['S3_SECRET']
s3_region_name = environ.get('S3_REGION', 'ca-central-1')
bucket_name = environ.get('S3_BUCKET', 'vanhacks2018')

s3 = boto3.resource('s3', region_name=s3_region_name, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
client = boto3.client('s3', region_name=s3_region_name, aws_access_key_id=access_key, aws_secret_access_key=secret_key)


def uploadImageToS3(img_data, ext):
    key = f'{str(uuid.uuid4())}.{ext}'

    client.put_object(Bucket=bucket_name, Key=key, Body=img_data, ACL='public-read')
    return f'http://s3-{s3_region_name}.amazonaws.com/{bucket_name}/{key}'


@celery.task
def process_event(name, image_data, lat, lng, comment):
    models.initdb(environ['DATABASE_URL'])

    logging.info('Processing event')

    image_url = uploadImageToS3(image_data, 'jpg')
    logging.info('Event image uploaded to %s', image_url)

    event = models.Event(name, image_url, lat, lng, comment)
    event.save()

    logging.info('Event %s created', event.id)
    
    models._conn.close()
    external_service = environ.get('EXTERNAL_SERVICE_NOTIFY_ENDPOINT')
    if external_service:
        notify_external.apply_async(
            args=(external_service, event.id, image_url, lat, lng, comment)
        )


@celery.task
def notify_external(url, id, image_url, lat, lng, comment):
    requests.post(url, json={
        'event_id': id,
        'image_url': image_url,
        'position': [lat, lng],
        'comment': comment,
    })
