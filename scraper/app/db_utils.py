"""
Module for database settings and its initialization.
"""
import os
import shutil
from sqlalchemy import exc
from werkzeug.exceptions import HTTPException
from definitions import ROOT_DIR, IMAGES_DIR_NAME
from app import db, ma


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
        app.register_error_handler(DatabaseException, 500)


def commit_to_database():
    """
    Function to commit to the database and handle exceptions.
    """
    try:
        db.session.commit()
    except exc.SQLAlchemyError:
        db.session.rollback()
        raise DatabaseException


class DatabaseException(HTTPException):
    """
    Raised when database transaction went wrong
    """
    code = 500
    description = 'Database transaction went wrong. Try using different data.'
    pass
