import os


def allow(fn):
    def inner(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        return fn(self, req, resp)
    return inner
