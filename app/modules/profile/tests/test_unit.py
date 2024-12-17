import pytest

from app import db
from app.modules.auth.repositories import UserRepository
from app.modules.conftest import login, logout
from app.modules.auth.models import User
from app.modules.profile.models import UserProfile
from app.modules.profile.services import UserProfileService


@pytest.fixture(scope="module")
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    for module testing (por example, new users)
    """
    with test_client.application.app_context():
        user_test = User(email='user@example.com', password='test1234')
        db.session.add(user_test)
        db.session.commit()

        profile = UserProfile(user_id=user_test.id, name="Name", surname="Surname")
        db.session.add(profile)
        db.session.commit()

    yield test_client


def test_edit_profile_page_get(test_client):
    """
    Tests access to the profile editing page via a GET request.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.get("/profile/edit")
    assert response.status_code == 200, "The profile editing page could not be accessed."
    assert b"Edit profile" in response.data, "The expected content is not present on the page"

    logout(test_client)


def test_get_view_user_profile(test_client):

    response = test_client.get("/profile/1")
    assert response.status_code == 200, "The profile editing page not was accesed."


def test_get_view_user_profile_does_not_exist(test_client):

    response = test_client.get("/profile/123456789")
    assert response.status_code == 404, "The profile editing page was accesed, which should not happen."


def test_edit_profile_become_developer_success(test_client):
    """
    Tests the successful transition of a normal user to a developer.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was successful."

    data = {
        "name": "Test1",
        "surname": "Foo1",
        "orcid": "",
        "affiliation": "",
        "is_developer": True,
        "github_username": "dummy_username"
    }
    user_id = UserRepository().get_by_email("user@example.com").id

    UserProfileService().update_profile(user_id, **data)

    assert UserRepository().get_by_id(user_id).is_developer
    assert UserRepository().get_by_id(user_id).github_username == "dummy_username"


def test_edit_profile_become_developer_no_github_username(test_client):
    """
    Tests the transition of a normal user to a developer without a GitHub username.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was successful."

    data = {
        "name": "Test1",
        "surname": "Foo1",
        "orcid": "",
        "affiliation": "",
        "is_developer": True,
        "github_username": ""
    }
    user_id = UserRepository().get_by_email("user@example.com").id

    with pytest.raises(ValueError, match="Developer must have a GitHub username."):
        UserProfileService().update_profile(user_id, **data)
