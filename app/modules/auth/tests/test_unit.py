import pytest
from flask import url_for

from app.modules.auth.services import AuthenticationService
from app.modules.auth.repositories import UserRepository
from app.modules.profile.repositories import UserProfileRepository


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


def test_login_success(test_client):
    response = test_client.post(
        "/login", data=dict(email="test@example.com", password="test1234"), follow_redirects=True
    )

    assert response.request.path != url_for("auth.login"), "Login was unsuccessful"

    test_client.get("/logout", follow_redirects=True)


def test_login_unsuccessful_bad_email(test_client):
    response = test_client.post(
        "/login", data=dict(email="bademail@example.com", password="test1234"), follow_redirects=True
    )

    assert response.request.path == url_for("auth.login"), "Login was unsuccessful"

    test_client.get("/logout", follow_redirects=True)


def test_login_unsuccessful_bad_password(test_client):
    response = test_client.post(
        "/login", data=dict(email="test@example.com", password="basspassword"), follow_redirects=True
    )

    assert response.request.path == url_for("auth.login"), "Login was unsuccessful"

    test_client.get("/logout", follow_redirects=True)


def test_signup_user_no_name(test_client):
    response = test_client.post(
        "/signup", data=dict(surname="Foo", email="test@example.com", password="test1234"), follow_redirects=True
    )
    assert response.request.path == url_for("auth.show_signup_form"), "Signup was unsuccessful"
    assert b"This field is required" in response.data, response.data


def test_signup_user_unsuccessful(test_client):
    email = "test@example.com"
    response = test_client.post(
        "/signup", data=dict(name="Test", surname="Foo", email=email, password="test1234"), follow_redirects=True
    )
    assert response.request.path == url_for("auth.show_signup_form"), "Signup was unsuccessful"
    assert f"Email {email} in use".encode("utf-8") in response.data


def test_signup_user_successful(test_client):
    response = test_client.post(
        "/signup",
        data=dict(name="Foo", surname="Example", email="foo@example.com", password="foo1234"),
        follow_redirects=True,
    )
    assert response.request.path == url_for("auth.login"), "Signup was unsuccessful"


def test_service_create_with_profie_success(clean_database):
    data1 = {
        "name": "Test1",
        "surname": "Foo1",
        "email": "service_test1@example.com",
        "password": "test1234",
        "is_developer": False,
        "github_username": ""
    }

    data2 = {
        "name": "Test2",
        "surname": "Foo2",
        "email": "service_test2@example.com",
        "password": "test1234",
        "is_developer": True,
        "github_username": "Ensaladilla_lover"
    }

    data3 = {
        "name": "Test3",
        "surname": "Foo3",
        "email": "service_test3@example.com",
        "password": "test1234",
        "is_developer": False,
        "github_username": "Croqueta_lover"
    }

    AuthenticationService().create_with_profile(**data1)
    AuthenticationService().create_with_profile(**data2)
    AuthenticationService().create_with_profile(**data3)

    assert UserRepository().count() == 3
    assert UserProfileRepository().count() == 3


def test_service_create_with_profile_fail_no_email(clean_database):
    data = {
        "name": "Test",
        "surname": "Foo",
        "email": "",
        "password": "1234",
        "is_developer": False,
        "github_username": ""
    }

    with pytest.raises(ValueError, match="Email is required."):
        AuthenticationService().create_with_profile(**data)

    assert UserRepository().count() == 0
    assert UserProfileRepository().count() == 0


def test_service_create_with_profile_fail_no_password(clean_database):
    data = {
        "name": "Test",
        "surname": "Foo",
        "email": "test@example.com",
        "password": "",
        "is_developer": False,
        "github_username": ""
    }

    with pytest.raises(ValueError, match="Password is required."):
        AuthenticationService().create_with_profile(**data)

    assert UserRepository().count() == 0
    assert UserProfileRepository().count() == 0


def test_service_create_with_developer_fail_no_github_username(clean_database):
    data = {
        "name": "Test",
        "surname": "Foo",
        "email": "test@example.com",
        "password": "1234",
        "is_developer": True,
        "github_username": ""
    }

    with pytest.raises(ValueError, match="Developer must have a GitHub username."):
        AuthenticationService().create_with_profile(**data)

    assert UserRepository().count() == 0
    assert UserProfileRepository().count() == 0


# Sign up verification tests
def test_login_unverified_email(test_client, clean_database):
    test_signup_user_successful(test_client)
    response_login = test_client.post(
        "/login", data=dict(email="foo@example.com", password="foo1234"), follow_redirects=True
    )

    assert response_login.request.path == url_for("auth.login"), "Login was succesful"


def test_login_verified_email_bad_token(test_client, clean_database):
    test_signup_user_successful(test_client)

    user = UserRepository().get_by_email("foo@example.com")
    token = AuthenticationService().generate_confirmation_token(user.id)

    response_verified_email = test_client.get(
        f"/confirm/{token}ewrerww", follow_redirects=True
    )

    response_login = test_client.post(
        "/login", data=dict(email="foo@example.com", password="foo1234"), follow_redirects=True
    )

    assert response_verified_email.request.path == url_for("public.index"), "Verification was successful"
    assert response_login.request.path == url_for("auth.login"), "Login was succesful"


def test_login_verified_email_good_token(test_client, clean_database):
    test_signup_user_successful(test_client)

    user = UserRepository().get_by_email("foo@example.com")
    token = AuthenticationService().generate_confirmation_token(user.id)

    response_verified_email = test_client.get(
        f"/confirm/{token}", follow_redirects=True
    )

    response_login = test_client.post(
        "/login", data=dict(email="foo@example.com", password="foo1234"), follow_redirects=True
    )

    assert response_verified_email.request.path == url_for("auth.login"), "Verification was unsuccessful"
    assert response_login.request.path == url_for("public.index"), "Login was unsuccesful"
