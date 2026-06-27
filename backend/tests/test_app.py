# backend/tests/test_app.py

import io
from unittest.mock import patch

import pytest

from backend.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


class TestApp:

    def test_allowed_file_csv(self):
        from backend.app import allowed_file

        assert allowed_file("ecg.csv") is True

    def test_allowed_file_non_csv(self):
        from backend.app import allowed_file

        assert allowed_file("ecg.txt") is False
        assert allowed_file("ecg") is False

    def test_upload_without_file(self, client):
        response = client.post("/upload")

        assert response.status_code == 302

    def test_upload_empty_filename(self, client):
        response = client.post(
            "/upload",
            data={
                "file": (io.BytesIO(b"dummy"), "")
            },
            content_type="multipart/form-data",
        )

        assert response.status_code == 302

    def test_upload_bad_extension(self, client):
        response = client.post(
            "/upload",
            data={
                "file": (io.BytesIO(b"dummy"), "ecg.txt")
            },
            content_type="multipart/form-data",
        )

        assert response.status_code == 422

        data = response.get_json()

        assert data["message"] == "bad file format"

    @patch("backend.app.process_ecg")
    def test_upload_valid_csv(self, mock_process_ecg, client):

        mock_process_ecg.return_value = (
            60.0,
            (50.0, 100.0, 1300.0),
            (80.0, 1300.0, 2100.0),
        )

        response = client.post(
            "/upload",
            data={
                "file": (
                    io.BytesIO(
                        b"QRS,100,120\nQRS,1100,1120\n"
                    ),
                    "ecg.csv",
                )
            },
            content_type="multipart/form-data",
        )

        assert response.status_code == 201

        data = response.get_json()

        assert data["message"] == "ok"
        assert data["mean_cycle"] == 60.0

        # Flask JSON converts tuples to lists
        assert data["min_cycle"] == [50.0, 100.0, 1300.0]
        assert data["max_cycle"] == [80.0, 1300.0, 2100.0]

        mock_process_ecg.assert_called_once()

    def test_index_route(self, client):
        response = client.get("/")

        # If frontend build exists -> 200
        # Otherwise -> 404
        assert response.status_code in (200, 404)