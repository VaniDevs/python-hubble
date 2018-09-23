import http
import requests
import yaml
import logging

logger = logging.getLogger(__name__)
settings = {}


def load_from_url(url):
    if url is None:
        return

    resp = requests.get(url)
    if resp.status_code == http.HTTPStatus.OK:
        data = yaml.load(resp.content)
        logger.info(f'Loaded client settings:\n{data}')
        settings.update(data)
    else:
        logger.warn(f'Unable to load config from {url}')
