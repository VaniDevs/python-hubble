import json


class Model:
    def to_dict(self):
        return self.__dict__


class User(Model):
    def __init__(self, name, email):
        self.name = name
        self.email = email

    @staticmethod
    def all():
        return _USERS.values()

    @staticmethod
    def get(key):
        return _USERS[key]


# just for testing
_USERS = {
    'foo': User('foo', 'foo@baz.com'),
    'bar': User('bar', 'bar@baz.com'),
}
