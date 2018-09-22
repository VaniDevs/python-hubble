import falcon
import os
from hubble import resources, models


def create_app(config):
    models.initdb(os.environ['DATABASE_URL'])

    app = falcon.API()
    app.add_route('/events', resources.Event())
    send_update = resources.SendUpdate()
    app.add_route('/send_update', send_update)
    return app
