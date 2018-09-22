FROM python:3.7.0-stretch

ENV LOG_LEVEL=warn

WORKDIR /api
COPY . /api
RUN pip install -e .

CMD gunicorn --log-level=${LOG_LEVEL} -b 0:8000 snitch.wsgi
