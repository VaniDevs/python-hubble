import falcon
import json


class HelloWorld:
    def on_get(self, req, resp, key=None):
        if key is None:
            resp.media = json.dumps({'hello': 'world'})
        else:
            resp.media = json.dumps({'hello': key})
