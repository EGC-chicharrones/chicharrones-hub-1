import pytest
from app.modules.conftest import login
from app import db
from app.modules.dataset.models import DataSet, DSMetaData, Author, PublicationType


@pytest.fixture(scope="module")
def test_client(test_client):
    with test_client.application.app_context():
        # Preparar datos de prueba
        author = Author(name="Author 1", affiliation="Affiliation 1", orcid="0000-0000-0000-0000")
        db.session.add(author)

        ds_meta_data = DSMetaData(
            title="Dataset 1",
            description="Description for dataset 1",
            publication_type=PublicationType.DATA_MANAGEMENT_PLAN,
            tags="tag1, tag2",
            rating_avg=4.5  # Asignamos un rating válido
        )
        db.session.add(ds_meta_data)

        dataset = DataSet(
            user_id=1,
            ds_meta_data=ds_meta_data
        )
        db.session.add(dataset)
        db.session.commit()

    yield test_client


# Test para un autor inexistente
def test_filter_by_nonexistent_author(test_client):
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login fue exitoso."

    response = test_client.get("/explore?query=author:asdasda")

    assert response.status_code == 200, "La respuesta fue exitosa."

    response_data = response.get_json()
    assert response_data is None


def test_filter_by_invalid_rating(test_client):
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login fue exitoso."

    response = test_client.get("/explore?query=rating:invalid_rating")

    response_data = response.get_json()
    assert response_data is None


def test_filter_with_empty_query(test_client):
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login fue exitoso."

    response = test_client.get("/explore?query=")

    response_data = response.get_json()
    assert response_data is None


def test_filter_with_invalid_query_format(test_client):
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login fue exitoso."

    response = test_client.get("/explore?query=author:")

    response_data = response.get_json()
    assert response_data is None


def test_filter_by_multiple_criteria_no_results(test_client):
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login fue exitoso."

    response = test_client.get("/explore?query=author:Nonexistent Author&query=rating:999")

    assert response.status_code == 200, "La respuesta fue exitosa."

    response_data = response.get_json()
    assert response_data is None


def test_filter_with_multiple_invalid_criteria(test_client):
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login fue exitoso."

    response = test_client.get("/explore?query=author:&query=rating:invalid_rating")

    response_data = response.get_json()
    assert response_data is None
