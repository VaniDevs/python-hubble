import falcon
from hubble import resources, models


def create_app(config):
    models.initdb(os.environ['DATABASE_URL'])

    app = falcon.API()
    app.add_route('/events', resources.Events())
    return app
