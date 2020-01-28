"""
Module with API classes.
"""
from flask import send_file, Response, stream_with_context
from flask_restful import Resource, Api
from sqlalchemy.orm.exc import NoResultFound
from app.tasks import get_data_from_url
from app.models import Url, TextContent
from app.schema import UrlSchema
from app import db, celery
from definitions import ROOT_DIR, IMAGES_DIR_NAME
from io import StringIO
import os


api = Api()


class GetUrlContents(Resource):
    """
    API class used for starting a new task which saves URL content and its name in the system.
    """
    def post(self, name, url):
        """
        POST request method for class GetUrlContents
        URL: '/url/<name>/<url>'
        :param name: Name used for identifying content in the system
        :param url: URL which content will be saved in the system
        :return: Task ID of the started task
        """
        new_url_object = Url(name=name.encode("utf-8"), url=url.encode("utf-8"))
        db.session.add(new_url_object)
        db.session.commit()
        url_schema = UrlSchema()
        result = get_data_from_url.delay(url_schema.dump(new_url_object))
        return f"Task started. Task ID: {result}", 200


class GetTaskStatus(Resource):
    """
    API class used for checking the task status.
    To start a new task please refer to "GetUrlContents" class.
    """
    def get(self, task_id):
        """
        GET request method for class GetTaskStatus
        URL: '/status/<task_id>'
        :param task_id: task id returned after starting POST request GetUrlContents
        :return: Task ID and its status
        """
        result = celery.AsyncResult(task_id)
        return f"Task ID {task_id} state is: {result.state}", 200


class DownloadFile(Resource):
    """
    API class used for downloading files from the system.
    To put files in the system please refer to "GetUrlContents" class.
    """
    def get(self, name, file_type):
        """
        GET request method for class DownloadFile
        URL: '/download/<name>/<file_type>'
        :param name: Name of the URL contents on in the database
        :param file_type: "text" or "images" - content type which will be downloaded
        :return: File attachment or status.
        """
        if file_type == "images":
            try:
                filepath = os.path.join(ROOT_DIR, IMAGES_DIR_NAME, f'{name}.tar')
                return send_file(filepath, as_attachment=True)
            except FileNotFoundError:
                return f"File not found for '{name}' URL contents.", 204
        elif file_type == "text":
            try:
                url_id = db.session.query(Url.id).filter(Url.name == name).one()[0]
                text_content = db.session.query(TextContent.text).filter(TextContent.url_id == url_id).one()[0]
                response = Response(stream_with_context(DownloadFile.generate_text(text_content)))
                response.headers['Content-Disposition'] = f'attachment; filename={name}.txt'
            except NoResultFound:
                return f"File not found for '{name}' URL contents.", 204
        else:
            response = Response("Please specify file type as 'text' or 'images'", 400)
        return response

    @staticmethod
    def generate_text(text_content: str) -> str:
        """
        Generator function allowing to stream string line by line.
        """
        for line in StringIO(text_content):
            yield line


api.add_resource(GetTaskStatus, '/status/<task_id>')
api.add_resource(GetUrlContents, '/url/<name>/<path:url>')
api.add_resource(DownloadFile, '/download/<name>/<file_type>')
