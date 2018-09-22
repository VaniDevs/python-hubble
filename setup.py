import os.path
import setuptools


with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as req:
    requirements = req.readlines()

with open(os.path.join(os.path.dirname(__file__), 'requirements-dev.txt')) as req_dev:
    requirements_devel = req_dev.readlines()


setuptools.setup(
    name='snitch',
    version='0.1.0',
    install_requires=requirements,
)
