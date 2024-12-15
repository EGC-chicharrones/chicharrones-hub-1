import pytest  # type: ignore
import os

from app import db
from app.modules.auth.models import User
from app.modules.dataset.models import DSMetaData, DSMetrics, DataSet, PublicationType
from app.modules.dataset.services import DataSetService
from app.modules.fakenodo.services import FakenodoService
from app.modules.featuremodel.models import FMMetaData, FeatureModel
from app.modules.fakenodo.services import checksum


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

        fm_meta_data_test_1 = FMMetaData(
            uvl_filename="test_file.uvl",
            title="Test Feature Model",
            description="Description for test feature model",
            publication_type=PublicationType.DATA_MANAGEMENT_PLAN,
            publication_doi="10.1234/fm.doi",
            tags="test",
            uvl_version="1.0"
        )

        # Crear FeatureModel asociado al dataset
        feature_model_test_1 = FeatureModel(
            data_set_id=1,
            fm_meta_data=fm_meta_data_test_1
        )

        # Crear un segundo dataset con su FeatureModel
        ds_meta_data_test_2 = DSMetaData(
            deposition_id=43,
            title="Second Test dataset",
            description="Second Test dataset",
            publication_type=PublicationType.DATA_MANAGEMENT_PLAN,
            publication_doi="10.1234/second.doi",
            dataset_doi="10.1234/second.dataset.doi",
            tags="second-test",
            ds_metrics=ds_metrics_test
        )

        dataset_test_2 = DataSet(
            user_id=1,
            ds_meta_data_id=2
        )

        fm_meta_data_test_2 = FMMetaData(
            uvl_filename="test_file.zip",
            title="Second Test Feature Model",
            description="Description for second test feature model",
            publication_type=PublicationType.DATA_MANAGEMENT_PLAN,
            publication_doi="10.1234/second.fm.doi",
            tags="second-test",
            uvl_version="1.0"
        )

        feature_model_test_2 = FeatureModel(
            data_set_id=2,
            fm_meta_data=fm_meta_data_test_2
        )

        # Agregar todo a la base de datos
        db.session.add_all([
            ds_metrics_test,
            ds_meta_data_test_1,
            dataset_test_1,
            fm_meta_data_test_1,
            feature_model_test_1,
            ds_meta_data_test_2,
            dataset_test_2,
            fm_meta_data_test_2,
            feature_model_test_2
        ])
        db.session.commit()

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


def test_upload_file_success_io(test_client):
    """
    Test successful file upload for a deposition.
    """
    fakenodo_service = FakenodoService()
    dataset_service = DataSetService()

    dataset = dataset_service.get_by_id(1)
    feature_model = FeatureModel.query.filter_by(data_set_id=1).first()

    user = User.query.filter_by(email='user@example.com').first()
    assert user is not None, "Test user not found in the database"
    # Prepare mock file for testing
    uvl_filename = "test_file.uvl"
    user_id = user.id
    file_path = f"./uploads/user_{user_id}/dataset_{dataset.id}/{uvl_filename}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write("Mock content for testing file upload.")

    deposition = fakenodo_service.upload_file(dataset, 42, feature_model, user=user)

    assert deposition["id"] == 42
    assert deposition["file"] == uvl_filename
    assert deposition["fileSize"] == os.path.getsize(file_path)
    assert deposition["checksum"] == checksum(file_path)
    assert deposition["message"] == "File Uploaded to deposition with id 42"

    # Cleanup
    os.remove(file_path)


def test_upload_file_success_zip(test_client):
    """
    Test successful file upload for a deposition.
    """
    fakenodo_service = FakenodoService()
    dataset_service = DataSetService()

    dataset = dataset_service.get_by_id(2)
    feature_model = FeatureModel.query.filter_by(data_set_id=2).first()

    user = User.query.filter_by(email='user@example.com').first()
    assert user is not None, "Test user not found in the database"

    # Prepare mock .zip file for testing
    zip_filename = "test_file.zip"
    user_id = user.id
    file_path = f"./uploads/user_{user_id}/dataset_{dataset.id}/{zip_filename}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(b"Mock content for testing zip file upload.")

    fakenodo_service.upload_file(dataset, 43, feature_model, user=user)

    # Cleanup
    os.remove(file_path)


def test_upload_file_not_assigned(test_client):
    """
    Test failing to upload a file for a deposition because no file is provided.
    """
    fakenodo_service = FakenodoService()
    dataset_service = DataSetService()

    dataset = dataset_service.get_by_id(3)
    feature_model = FeatureModel.query.filter_by(data_set_id=3).first()

    user = User.query.filter_by(email='user@example.com').first()
    assert user is not None, "Test user not found in the database"

    try:
        # Intentar subir un archivo sin pasar ningún archivo
        fakenodo_service.upload_file(dataset, 44, feature_model, user=user)
        assert False
    except Exception as e:
        # Comprobar que se lanza la excepción esperada
        assert str(e) == "'NoneType' object has no attribute 'fm_meta_data'"
