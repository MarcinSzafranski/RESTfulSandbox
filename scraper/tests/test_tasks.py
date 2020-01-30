import pytest
import os
from tarfile import TarError
from unittest.mock import patch, MagicMock, Mock
from app.db_utils import DatabaseException
from app.tasks import tar_images, get_data_from_url, parse_and_add_data_to_database
from conftest import MockTaskResponse, MockUrlSchema, mocked_requests_get
from definitions import TESTS_DIR_NAME, IMAGES_DIR_NAME


class TestGetDataFromUrl:
    def test_success(self, app, monkeypatch):
        schema = MockUrlSchema()
        Url = Mock()
        Url.url = "http://correct_url.com/"
        Url.name = "test_html"

        def mockreturn(*args, **kwargs):
            return MockTaskResponse()

        monkeypatch.setattr(parse_and_add_data_to_database, 'delay', mockreturn)
        monkeypatch.setattr(tar_images, 'delay', mockreturn)

        with app.app_context():
            with patch('app.tasks.requests.get') as requestsGetMock:
                requestsGetMock.side_effect = mocked_requests_get
                get_data_from_url(schema.dump(Url))
                requestsGetMock.assert_called_with(Url.url)

    def test_exception(self, app, monkeypatch):
        schema = MockUrlSchema()
        Url = Mock()
        Url.url = "incorrect_url"
        Url.name = "test_html"

        def mockreturn(*args, **kwargs):
            return MockTaskResponse()

        monkeypatch.setattr(parse_and_add_data_to_database, 'delay', mockreturn)
        monkeypatch.setattr(tar_images, 'delay', mockreturn)

        with app.app_context():
            with patch('app.tasks.requests.get') as requestsGetMock:
                requestsGetMock.side_effect = mocked_requests_get
                with pytest.raises(Exception):
                    get_data_from_url(schema.dump(Url))
                    requestsGetMock.assert_called_with(Url.url)


class TestParseAndAddDataToDatabase:
    def test_success(self, app):
        schema = MockUrlSchema()
        Url = Mock()
        Url.url = "www.test_url.com"
        Url.name = "test_html"

        with app.app_context():
            with open(os.path.join(TESTS_DIR_NAME, 'test_html.html')) as html_test_file:
                with patch('app.tasks.commit_to_database') as commitMock:
                    parse_and_add_data_to_database(html_test_file, schema.dump(Url))
                    commitMock.assert_called_once()

    def test_exception(self, app):
        schema = MockUrlSchema()
        Url = Mock()
        Url.url = "www.test_url.com"
        Url.name = "test_html"

        with app.app_context():
            with open(os.path.join(TESTS_DIR_NAME, 'test_html.html')) as html_test_file:
                with patch('app.tasks.commit_to_database') as commitMock:
                    commitMock.side_effect = DatabaseException
                    with pytest.raises(DatabaseException):
                        parse_and_add_data_to_database(html_test_file, schema.dump(Url))


class TestTarImages:
    @patch("tarfile.open")
    def test_success(self, mock_open):
        name = "some_test_name"
        mock_add = MagicMock()
        mock_open.return_value.__enter__.return_value.add = mock_add
        filename = os.path.join(IMAGES_DIR_NAME, f'{name}.tar')
        tar_images(name)
        mock_open.assert_called_with(filename, "w")
        mock_add.assert_called_with(os.path.join(IMAGES_DIR_NAME, name))

    @patch("tarfile.open")
    def test_exception(self, mock_open):
        name = "some_test_name"
        mock_open.side_effect = TarError
        with pytest.raises(TarError):
            tar_images(name)

