import pytest
from app.modules.conftest import login
from io import BytesIO


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

    
def test_chatbot_logged_in(test_client):
    """
    Test to access chatbot when the user is logged in.
    """
    login_response = login(test_client, "user1@example.com", "1234")
    assert login_response.status_code == 200, "Login was successful."

    response = test_client.get("/dataset/chatbot")
    assert response.status_code == 302


def test_chatbot_logged_out(test_client):
    """
    Test to access chatbot when the user is logged out.
    """
    response = test_client.get("/dataset/chatbot")

    assert response.status_code == 302, "Acceso denegado, redirigiendo al login."
    assert b"login" in response.data, "La redirección debe ser hacia la página de login."

def test_download_all_datasets(test_client):
    """
    Test to verify that /dataset/download/all works correctly.
    """
    response = test_client.get("/dataset/download/all", follow_redirects=True)

    assert response.status_code == 200, "The query has to be successful"
    assert response.content_type == "application/zip", "The file type must be a ZIP."
    assert len(response.data) > 0, "The ZIP file must not be empty."