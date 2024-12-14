import pytest

from app import db
from app.modules.auth.models import User
from app.modules.dataset.models import DSMetaData, DSMetrics, DataSet, PublicationType
from app.modules.dataset.services import DataSetService
from app.modules.fakenodo.services import FakenodoService
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
            number_of_models="1",
            number_of_features="1"
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

        dataset_test_1 = DataSet(
            user_id=1,
            ds_meta_data_id=1
        )

        feature_model_test_1 = FeatureModel(
            data_set_id=1
        )

        db.session.add_all([ds_metrics_test, ds_meta_data_test_1, dataset_test_1, feature_model_test_1])
        db.session.commit()
        pass

    yield test_client


def test_create_fakenodo_deposition_success(test_client):
    """
    Test creating a deposition in Fakenodo successfully. Takes an existing dataset.
    """
    fakenodo_service = FakenodoService()
    dataset_service = DataSetService()

    dataset_1 = dataset_service.get_by_id(1)
    deposition = fakenodo_service.create_new_deposition(dataset_1)

    assert deposition["metadata"]["title"] == "Test dataset"
    assert deposition["metadata"]["description"] == "Test dataset"
    assert deposition["id"] == 1


def test_create_fakenodo_deposition_fail_nonexistent_dataset(test_client):
    """
    Test failing to create a deposition in Fakenodo because the dataset with ID 20241214 does not exist.
    """
    fakenodo_service = FakenodoService()
    dataset_service = DataSetService()

    try:
        dataset = dataset_service.get_by_id(20241214)
        fakenodo_service.create_new_deposition(dataset)
        assert False
    except Exception as e:
        assert str(e) == "'NoneType' object has no attribute 'ds_meta_data'"


def test_publish_deposition_success(test_client):
    """
    Test publishing a deposition in Fakenodo. Takes an existing deposition.
    """
    fakenodo_service = FakenodoService()

    # It is necessary to create a deposition before publishing it.
    # It is assumed that it was created in the previous test.
    response = fakenodo_service.publish_deposition(1)

    assert response["id"] == 1
    assert response["message"] == "Deposition published successfully in fakenodo."


def test_publish_deposition_fail_nonexistent_deposition(test_client):
    """
    Test failing to publish a deposition in Fakenodo because the deposition with ID 20241214 does not exist.
    """
    fakenodo_service = FakenodoService()

    try:
        fakenodo_service.publish_deposition(20241214)
        assert False
    except Exception as e:
        assert str(e) == "Error 404: Deposition not found"
