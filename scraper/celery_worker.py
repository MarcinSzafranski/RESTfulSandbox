"""
Module used for running Celery instance.
Example use:
In the virtualenv with all requirements installed use below command to start celery worker:

celery worker -A celery_worker.celery --loglevel=info -P solo
"""
from app import celery
from app.factory import create_app
from app.celery_utils import init_celery


app = create_app()
init_celery(celery, app)
