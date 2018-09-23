import falcon
import os

from hubble import resources, models, client_config


def create_app():
    models.initdb(os.environ['DATABASE_URL'])
    client_config.load_from_url(os.environ.get('CLIENT_CONFIG_URL'))

    app = falcon.API()
    app.add_route('/events', resources.Event())
    app.add_route('/client/config', resources.ClientConfig())
    return app
