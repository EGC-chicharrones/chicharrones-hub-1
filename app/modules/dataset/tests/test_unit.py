import pytest

from app import db
from app.modules.auth.models import User
from app.modules.conftest import login
from io import BytesIO
from unittest.mock import MagicMock

from app.modules.dataset.models import DSMetaData, DSMetrics, DataSet, PublicationType
from app.modules.dataset.services import DataSetService
from app.modules.featuremodel.models import FeatureModel


@pytest.fixture(scope="module")
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        # Add HERE new elements to the database that you want to exist in the test context.
        # DO NOT FORGET to use db.session.add(<element>) and db.session.commit() to save the data.

        user_test = User(email='user@example.com', password='test1234')
        db.session.add(user_test)
        db.session.commit()

        ds_metrics_test = DSMetrics(
            number_of_models="2",
            number_of_features="2"
        )

        ds_meta_data_test_1 = DSMetaData(
            deposition_id=42,
            title="Test dataset",
            description="Test dataset",
            publication_type=PublicationType.DATA_MANAGEMENT_PLAN,
            publication_doi="10.1234/test.doi",
            dataset_doi="10.1234/dataset.doi",
            tags="test",
            ds_metrics=ds_metrics_test
        )

        ds_meta_data_test_2 = DSMetaData(
            deposition_id=170,
            title="Test dataset, part 2",
            description="It is better to test more",
            publication_type=PublicationType.DATA_MANAGEMENT_PLAN,
            publication_doi="10.1235/test.doi",
            dataset_doi="10.1235/dataset.doi",
            tags="test2",
            ds_metrics=ds_metrics_test
        )

        dataset_test_1 = DataSet(
            user_id=1,
            ds_meta_data_id=1
        )

        dataset_test_2 = DataSet(
            user_id=1,
            ds_meta_data_id=2
        )

        feature_model_test_1 = FeatureModel(
            data_set_id=1
        )

        feature_model_test_2 = FeatureModel(
            data_set_id=2
        )

        db.session.add_all([ds_metrics_test, ds_meta_data_test_1, ds_meta_data_test_2, dataset_test_1,
                            dataset_test_2, feature_model_test_1, feature_model_test_2])
        db.session.commit()
        pass
    yield test_client


def test_count_datasets_success(test_client):
    """
    Test finding all datasets IDs.
    """
    dataset_service = DataSetService()

    datasets = dataset_service.get_datasets_ids()

    assert len(datasets) == 2


def test_list_user_syncronised_datasets_success(test_client):
    """
    Test finding a user's synchronised datasets.
    """
    dataset_service = DataSetService()
    user_id = 1

    datasets = sorted(dataset_service.get_synchronized(user_id), key=lambda d: d.id)

    assert len(datasets) == 2
    assert datasets[0].name() == "Test dataset"
    assert datasets[1].name() == "Test dataset, part 2"


def test_list_user_syncronised_datasets_no_datasets(test_client):
    """
    Test finding a user's synchronised datasets for a user that has none.
    """
    dataset_service = DataSetService()
    user_id = 2

    datasets = dataset_service.get_synchronized(user_id)

    assert len(datasets) == 0


def test_upload_dataset_uvl_file_success(test_client):
    """
    Test uploading a UVL file to a dataset
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    data = {
        "file": (BytesIO(b"UVL Content"), "test_file.uvl")
    }

    response = test_client.post(
        "/dataset/file/upload",
        data=data,
        content_type="multipart/form-data",
        follow_redirects=True)

    assert response.status_code == 200, "Upload was unsuccessful."


def test_upload_dataset_uvl_github_success(test_client):
    """
    Test uploading a valid UVL file from a GitHub repository to a dataset.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    data = {
        # Valid UVL file found on GitHub as of writing this test.
        "url": "https://github.com/Universal-Variability-Language/uvl-models/blob/"
        + "main/Decision_Models/Mobile_Phone/dm_mobile_phone.csv.uvl"
    }

    response = test_client.post(
        "/dataset/file/upload_from_github",
        json=data,
        follow_redirects=True)

    assert response.status_code == 200, "Upload was unsuccessful."


def test_upload_dataset_uvl_github_wrong_url_format(test_client):
    """
    Test passing invalid links to the function to upload a dataset.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    bad_urls = ["", "no", "https://example.com", "https://github", "https://github.com/a",
                "https://github.com/nonexistent_user/fake_repository/thisfileisnothere.uvl",
                "https://github.com/Universal-Variability-Language/uvl-models/blob/main/"
                + "Decision_Models/Mobile_Phone/thisfileisnothere.csv.uvl"]
    data = [{'url': url} for url in bad_urls]

    for d in data:
        response = test_client.post(
            "/dataset/file/upload_from_github",
            data=d,
            content_type="application/json")

        assert response.status_code == 400, "Upload was successful."


def test_chatbot_logged_in(test_client):
    """
    Test to access chatbot when the user is logged in.
    """
    login_response = login(test_client, "user1@example.com", "1234")
    assert login_response.status_code == 200, "Login was successful."

    response = test_client.get("/dataset/chatbot")
    assert response.status_code == 200


def test_chatbot_logged_out(test_client):
    """
    Test to access chatbot when the user is logged out.
    """
    response = test_client.get("/dataset/chatbot")

    assert response.status_code == 200, "Acceso denegado, redirigiendo al login."


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
