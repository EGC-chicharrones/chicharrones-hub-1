import pytest
from app.modules.conftest import login
from io import BytesIO
from unittest.mock import MagicMock


@pytest.fixture(scope="module")
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        # Add HERE new elements to the database that you want to exist in the test context.
        # DO NOT FORGET to use db.session.add(<element>) and db.session.commit() to save the data.
        pass
    yield test_client


def test_upload_dataset_success(test_client):
    """
    Test uploading a dataset
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was successful."

    data = {
        "file": (BytesIO(b"UVL Content"), "test_file.uvl")
    }

    response = test_client.post(
        "/dataset/file/upload",
        data=data,
        content_type="multipart/form-data",
        follow_redirects=True)

    assert response.status_code == 200, "Upload was successful."


def test_download_all_datasets(test_client):
    """
    Test to verify that /dataset/download/all works correctly.
    """
    response = test_client.get("/dataset/download/all", follow_redirects=True)

    assert response.status_code == 200, "The query has to be successful"
    assert response.content_type == "application/zip", "The file type must be a ZIP."
    assert len(response.data) > 0, "The ZIP file must not be empty."


def test_get_ratings_no_ratings(test_client):
    """
    Test the scenario when there are no ratings for a given dataset.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was successful."

    mock_repository = MagicMock()
    mock_repository.get_ratings_by_dataset_id.return_value = []

    dataset_id = 123
    ratings = mock_repository.get_ratings_by_dataset_id(dataset_id)

    assert ratings == [], f"Expected an empty list of ratings for dataset_id {dataset_id}."


def test_get_ratings_positive(test_client):
    """
    Test the scenario when there are ratings for a given dataset.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was successful."

    mock_repository = MagicMock()
    mock_repository.get_ratings_by_dataset_id.return_value = [
        {"rating": 5, "user_id": 1, "comment": "Excellent dataset!"},
        {"rating": 4, "user_id": 2, "comment": "Good dataset, needs improvement."}
    ]

    dataset_id = 123
    ratings = mock_repository.get_ratings_by_dataset_id(dataset_id)

    assert len(ratings) == 2, f"Expected 2 ratings for dataset_id {dataset_id}."
    assert ratings[0]["rating"] == 5, f"Expected rating 5 for the first rating, but got {ratings[0]['rating']}."
    assert ratings[1]["rating"] == 4, f"Expected rating 4 for the second rating, but got {ratings[1]['rating']}."
    assert ratings[0]["comment"] == "Excellent dataset!", "First comment mismatch."
    assert ratings[1]["comment"] == "Good dataset, needs improvement.", "Second comment mismatch."


def test_calculate_avg_rating_no_ratings(test_client):
    """
    Test the scenario when there are no ratings, so avg_rating should return None.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was successful."

    mock_repository = MagicMock()
    mock_repository.calculate_avg_rating.return_value = None

    dataset_id = 123
    avg_rating = mock_repository.calculate_avg_rating(dataset_id)

    assert avg_rating is None, f"Expected None as the average rating for dataset_id {dataset_id}, but got {avg_rating}."


def test_calculate_avg_rating_positive(test_client):
    """
    Test the scenario when the average rating is calculated successfully.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was successful."

    mock_repository = MagicMock()
    mock_repository.calculate_avg_rating.return_value = 4.5

    dataset_id = 123
    avg_rating = mock_repository.calculate_avg_rating(dataset_id)

    assert avg_rating == 4.5, f"Expected average rating of 4.5 for dataset_id {dataset_id}, but got {avg_rating}."
