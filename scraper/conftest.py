import pytest
import app
from app import factory
from celery import uuid
from unittest.mock import Mock
from marshmallow import Schema, fields
from definitions import SQLALCHEMY_TEST_DB_URI, SQLALCHEMY_TRACK_MODIFICATIONS

celery_app = app.celery


@pytest.fixture
def app(monkeypatch):
    """
    Creates new app instance for each test.
    """

    app = factory.create_app(test_config={"TESTING": True,
                                          "SQLALCHEMY_DATABASE_URI": SQLALCHEMY_TEST_DB_URI,
                                          "SQLALCHEMY_TRACK_MODIFICATIONS": SQLALCHEMY_TRACK_MODIFICATIONS},
                             celery=celery_app)

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


class MockTaskResponse:
    @property
    def task_id(self):
        task_id = uuid()
        return task_id


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, text, status_code):
            self.text_data = text
            self.status_code = status_code

        @property
        def ok(self):
            if self.status_code == 200:
                return True
            else:
                return False

        @property
        def text(self):
            return self.text_data

    if args[0] == 'http://correct_url.com/':
        return MockResponse("Some text data", 200)
    return MockResponse(None, 404)


def mock_accessor(schema, attr, obj, default=None):
    result = getattr(obj, attr, default)
    if isinstance(result, Mock().__class__):
        return default
    return result


class MockSchema(Schema):
    """A Schema that can serialize Mock objects."""
    __accessor__ = mock_accessor


class MockUrlSchema(MockSchema):
    name = fields.Str()
    url = fields.Url()
