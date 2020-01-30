"""
Configuration file with definitions of environment variables needed for the system to run properly.
"""
import os

APP_NAME = "ZADANIE"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TESTS_DIR_NAME = "tests"
IMAGES_DIR_NAME = "images"

FLASK_HOST = "0.0.0.0"

# CELERY
CELERY_DB_URI = "db+mysql+pymysql://root:root@db:3306/celery"
CELERY_BROKER = "amqp://admin:mypass@rabbitmq:5672"
CELERY_IMPORTS = ('app/tasks', )
CELERY_TASK_TRACK_STARTED = True
CELERY_IGNORE_RESULT = False

# SQLALCHEMY
SQLALCHEMY_DB_URI = "mysql+pymysql://root:root@db:3306/sqlalchemy?charset=utf8mb4&binary_prefix=true"
SQLALCHEMY_TEST_DB_URI = "sqlite:///:memory:"
SQLALCHEMY_TRACK_MODIFICATIONS = False

DOCKER_FLASK_URL = "http://192.168.99.100:5000/"
