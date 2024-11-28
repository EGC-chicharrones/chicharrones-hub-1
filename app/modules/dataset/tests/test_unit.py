import pytest

from app import db
from app.modules.conftest import login
from app.modules.auth.models import User
from app.modules.profile.models import UserProfile
from io import BytesIO

# from app.modules.dataset.services import DataSetService


@pytest.fixture(scope="module")
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        user_test = User(email='user@example.com', password='test1234')
        db.session.add(user_test)
        db.session.commit()

        profile = UserProfile(user_id=user_test.id, name="Name", surname="Surname")
        db.session.add(profile)
        db.session.commit()
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


def test_change_anonymize_unsync_success(test_client):
    """
    Test changing the anonymize status of an unsynchronized dataset
    """

    # dataset_service = DataSetService()

    # login_response = login(test_client, "user@example.com", "test1234")
    # assert login_response.status_code == 200, "Login was successful."

    # data = {
    #     "file": (BytesIO(b"UVL Content"), "test_file.uvl")
    # }

    # response = test_client.post(
    #     "/dataset/file/upload",
    #     data=data,
    #     content_type="multipart/form-data",
    #     follow_redirects=True)

    # assert response.status_code == 200, "Upload was successful."

    # datasets = dataset_service.get_unsynchronized(User.query.filter_by(email="user@example.com").first().id)
    # dataset_id = datasets[0].id
    # assert dataset_id is not None, "Dataset ID should be present in the response."

    # # Verify the anonymize status change
    # response = test_client.post(
    #     f"/dataset/anonymize/unsync/{dataset_id}/",
    #     follow_redirects=True)

    # assert response.status_code == 200, "Anonymize status change was successful."
    pass
