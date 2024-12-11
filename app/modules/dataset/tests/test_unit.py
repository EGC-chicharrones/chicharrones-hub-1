import pytest

from app import db
from app.modules.conftest import login
from io import BytesIO

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
        "url": "https://github.com/Universal-Variability-Language/uvl-models/blob/main/"
        + "Decision_Models/Mobile_Phone/dm_mobile_phone.csv.uvl"
    }

    response = test_client.post(
        "/dataset/file/upload_from_github",
        data=data,
        content_type="application/json",
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
