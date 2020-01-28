"""
Application factory module, contains create_app function which actually creates Flask app instance and initializes
API, database and celery app if celery argument is given.
"""
from flask import Flask
from app.celery_utils import init_celery
from app.db_utils import init_database
from app.api import api
from definitions import APP_NAME, SQLALCHEMY_DB_URI, SQLALCHEMY_TRACK_MODIFICATIONS


def create_app(app_name=APP_NAME, test_config=None, **kwargs):
    """
    Function which creates Flask app instance and initializes database, API, and celery when given celery argument.
    Only celery worker calls this function without celery argument given, for its purpose of having its own instances.
    :param app_name: Application name. Can be set in definitions file.
    :param test_config: -
    :param kwargs: keyword arguments which may contain 'celery' key with celery app instance as argument.
    :return: Flask app instance
    """
    app = Flask(app_name)
    if kwargs.get("celery"):
        init_celery(kwargs.get("celery"), app)

    if test_config:
        app.config.update(test_config)
    else:
        app.config.from_mapping(
            SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DB_URI,
            SQLALCHEMY_TRACK_MODIFICATIONS=SQLALCHEMY_TRACK_MODIFICATIONS,
        )

    with app.app_context():
        init_database(app)
        api.init_app(app)

    return app

