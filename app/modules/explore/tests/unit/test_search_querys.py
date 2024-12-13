import pytest
from app.modules.conftest import login
from app import db
from app.modules.dataset.models import DataSet, DSMetaData, Author, PublicationType


@pytest.fixture(scope="module")
def test_client(test_client):
    with test_client.application.app_context():
        author = Author(name="Author 1", affiliation="Affiliation 1", orcid="0000-0000-0000-0000")
        db.session.add(author)

        ds_meta_data = DSMetaData(
            title="Dataset 1",
            description="Description for dataset 1",
            publication_type=PublicationType.DATA_MANAGEMENT_PLAN,
            tags="tag1, tag2"
        )
        db.session.add(ds_meta_data)

        dataset = DataSet(
            user_id=1,
            ds_meta_data=ds_meta_data
        )
        db.session.add(dataset)
        db.session.commit()

    yield test_client


def test_filter_by_author(test_client):
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login fue exitoso."

    response = test_client.get("/explore?query=author:Author 1")

    assert response.status_code == 200, "La respuesta fue exitosa."


def test_filter_by_tag(test_client):
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login fue exitoso."

    response = test_client.get("/explore?query=tag:tag1")

    assert response.status_code == 200, "La respuesta fue exitosa."


def test_filter_by_rating(test_client):
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login fue exitoso."

    response = test_client.get("/explore?query=rating:5")

    assert response.status_code == 200, "La respuesta fue exitosa."


def test_filter_by_multiple_criteria(test_client):

    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login fue exitoso."

    response = test_client.get("/explore?query=author:Author 1&query=tag:tag1&query=rating:5")

    assert response.status_code == 200, "La respuesta fue exitosa."


def test_filter_by_nonexistent_author(test_client):
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login fue exitoso."

    response = test_client.get("/explore?query=author:Nonexistent Author")

    assert response.status_code == 200, "La respuesta fue exitosa."
    assert len(response.json) == 0, "No deberían encontrarse resultados."


def test_filter_by_nonexistent_rating(test_client):
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login fue exitoso."

    response = test_client.get("/explore?query=rating:999")

    assert response.status_code == 200, "La respuesta fue exitosa."
    assert len(response.json) == 0, "No deberían encontrarse resultados."


def test_filter_with_invalid_query_format(test_client):
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login fue exitoso."

    response = test_client.get("/explore?query=author:")

    assert response.status_code == 400, "Debería devolver un error de formato (400)."
    assert "error" in response.json, "El mensaje de error debería indicar un formato incorrecto."


def test_filter_by_multiple_criteria_success(test_client):
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login fue exitoso."

    response = test_client.get("/explore?query=author:Author 1&query=tag:tag1&query=rating:5")

    assert response.status_code == 200, "La respuesta fue exitosa."

    datasets = response.json
    assert len(datasets) > 0, "Debería haber al menos un dataset en los resultados."

    for dataset in datasets:
        assert "Author 1" in dataset["author"], "El autor no es el esperado."
        assert "tag1" in dataset["tags"], "El tag no es el esperado."
        assert dataset["rating"] == 5, "El rating no es el esperado."
