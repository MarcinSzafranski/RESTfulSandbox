"""
Module for Celery settings.
"""
from app import Task, db


def init_celery(celery, app):
    """
    Init function for celery related stuff, like setting custom Task classes.
    :param celery: Celery app instance
    :param app: Flask app instance
    :return:
    """
    celery.conf.update(app.config)

    class DBTask(Task):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return Task.__call__(self, *args, **kwargs)

        def after_return(self, *args, **kwargs):
            db.session.remove()
    celery.task_cls = DBTask

