from conftest import celery_app, MockTaskResponse
from app.api import get_data_from_url
from app.db_utils import DatabaseException
from unittest.mock import patch
from flask import send_file
from definitions import ROOT_DIR, TESTS_DIR_NAME
import pytest
import os


class TestGetTaskStatus:
    @pytest.mark.parametrize("state, status_code", [('PENDING', 400),
                                                    ('SUCCESS', 200),
                                                    ('SENT', 200),
                                                    ('FAILURE', 500),
                                                    ('REVOKE', 200)])
    def test_get_task_status(self, client, monkeypatch, state, status_code):
        """Test for GetTaskStatus if status codes are matching states"""
        monkeypatch.setattr(celery_app.AsyncResult, 'state', state)
        response = client.get('/status/task_id')
        assert response.status_code == status_code


class TestGetUrlContents:
    @pytest.mark.parametrize("name, url, status_code", [('Any', "www.google.com", 200),
                                                        (1234, "http://google.com", 200),
                                                        ('StarWars', "https://en.wikipedia.org/wiki/Star_Wars", 200),
                                                        ('wrong url', '', 404)])
    def test_success(self, client, monkeypatch, name, url, status_code):
        """Test for GetUrlContents without exceptions."""

        def mockreturn(*args, **kwargs):
            return MockTaskResponse()

        monkeypatch.setattr(get_data_from_url, 'delay', mockreturn)
        response = client.post(f'/url/{name}/{url}')
        assert response.status_code == status_code

    @pytest.mark.parametrize("name, url, status_code", [("over_one_hundred_characters_name" * 4, "database_Exception.com", 500)])
    def test_database_exception(self, client, name, url, status_code):
        """Test for GetUrlContents with database exception."""

        with patch('app.api.commit_to_database') as commitMock:
            commitMock.side_effect = DatabaseException
            response = client.post(f'/url/{name}/{url}')
            assert response.status_code == status_code


class TestDownloadFile:
    @pytest.mark.parametrize("name, file_type, status_code",
                             [("Any", "text", 204),
                              ('Star Wars', "images", 204),
                              ("over_one_hundred_characters_name" * 4, "wrong_type", 400)])
    def test_failure(self, client, name, file_type, status_code):
        """Test for DownloadFile"""
        response = client.get(f'/download/{name}/{file_type}')
        assert response.status_code == status_code

    @pytest.mark.parametrize("name, file_type, status_code",
                             [("name for text case", "text", 200),
                              ("test_archive", "images", 200)])
    def test_success(self, client, monkeypatch, name, file_type, status_code):
        """Test for DownloadFile"""

        def mock_send_file(*args, **kwargs):
            return send_file(os.path.join(ROOT_DIR, TESTS_DIR_NAME, f'{name}.tar'), as_attachment=True)

        monkeypatch.setattr('app.api.send_file', mock_send_file)
        with patch('app.api.DownloadFile.generate_text'):
            with patch('app.api.db.session') as QueryMock:
                QueryMock.return_value.filter.return_value.all.return_value = "some suitable text"
                response = client.get(f'/download/{name}/{file_type}')
                assert response.status_code == status_code
