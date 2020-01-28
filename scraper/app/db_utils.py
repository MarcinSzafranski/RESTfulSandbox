"""
Module for database settings and its initialization.
"""
from app import db, ma
from definitions import ROOT_DIR, IMAGES_DIR_NAME
import shutil
import os


def init_database(app):
    """
    Init function for database related stuff, dropping database records when called and creating empty database.
    :param app:
    :return:
    """

    # Removing files from previous instances of Flask app
    shutil.rmtree(os.path.join(ROOT_DIR, IMAGES_DIR_NAME), ignore_errors=True)

    with app.app_context():
        db.init_app(app)
        db.drop_all()
        from .models import Url, Image, TextContent
        db.create_all()
        ma.init_app(app)
