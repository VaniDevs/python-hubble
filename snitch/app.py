import falcon
from snitch import resources


def create_app(config):
    app = falcon.API()
    hello_world = resources.HelloWorld()
    app.add_route('/hello', hello_world)
    app.add_route('/hello/{key}', hello_world)
    return app
