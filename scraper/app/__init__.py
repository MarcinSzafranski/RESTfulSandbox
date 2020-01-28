"""
Initialization module for DataBase, Marshmallow, Celery and celery Task objects.
"""
from celery import Celery
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from definitions import CELERY_DB_URI, CELERY_BROKER, CELERY_IMPORTS, CELERY_TASK_TRACK_STARTED, CELERY_IGNORE_RESULT


def make_celery(app_name=__name__):
    return Celery(app_name,
                  backend=CELERY_DB_URI,
                  broker=CELERY_BROKER,
                  imports=CELERY_IMPORTS,
                  task_track_started=CELERY_TASK_TRACK_STARTED,
                  ignore_result=CELERY_IGNORE_RESULT
                  )


db = SQLAlchemy()
ma = Marshmallow()
celery = make_celery()
Task = celery.create_task_cls()
