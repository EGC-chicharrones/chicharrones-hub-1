import pytest
from app import db
from app.modules.conftest import login
from app.modules.dataset.models import DataSet, DSMetaData, PublicationType
from app.modules.featuremodel.models import FeatureModel
from app.modules.hubfile.models import Hubfile


@pytest.fixture(scope="module")
def test_client(test_client):
    with test_client.application.app_context():
        # Crear dataset y metadatos
        ds_meta_data = DSMetaData(
            title="Test Dataset",
            description="Dataset for testing filters",
            publication_type=PublicationType.DATA_MANAGEMENT_PLAN,
            tags="test, dataset",
            dataset_doi="10.1234/datasetTest",
        )
        db.session.add(ds_meta_data)

        dataset = DataSet(user_id=1, ds_meta_data=ds_meta_data)
        db.session.add(dataset)
        db.session.flush()  # Generar ID del dataset

        feature_model = FeatureModel(data_set_id=dataset.id, features=10, constraints=5)
        db.session.add(feature_model)
        db.session.flush()

        hubfile = Hubfile(name="file1.uvl", checksum="123", size=12, feature_model_id=feature_model.id)
        db.session.add(hubfile)
        db.session.commit()

    yield test_client


def test_filter_by_features(test_client):
    # Realizar el login
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login fue exitoso."

    # Configurar el payload para la solicitud POST
    payload = {
        "constraints": "",
        "features": "10",
        "models": "",
        "publication_type": "any"
    }

    response = test_client.post("/explore", json=payload)
    assert response.status_code == 200, "La respuesta fue exitosa."

    # Convertir la respuesta JSON a un objeto de Python
    datasets = response.get_json()
    assert datasets is not None, "La respuesta debe contener datos en formato JSON."

    assert len(datasets) == 1, "Debe haber exactamente un dataset en los resultados."


def test_filter_by_features_no_result(test_client):
    # Realizar el login
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login fue exitoso."

    # Configurar el payload para la solicitud POST
    payload = {
        "constraints": "",
        "features": "1234567890",
        "models": "",
        "publication_type": "any"
    }

    response = test_client.post("/explore", json=payload)
    assert response.status_code == 200, "La respuesta fue exitosa."

    # Convertir la respuesta JSON a un objeto de Python
    datasets = response.get_json()
    assert datasets is not None, "La respuesta debe contener datos en formato JSON."

    assert len(datasets) == 0, "Debe haber exactamente ningún dataset en los resultados."


def test_filter_by_features_wrong_input(test_client):
    # Realizar el login
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login fue exitoso."

    # Configurar el payload para la solicitud POST
    payload = {
        "constraints": "",
        "features": "ERRÓNEO",
        "models": "",
        "publication_type": "any"
    }

    try:
        test_client.post("/explore", json=payload)
        assert False, "Se esperaba una ValueError pero no se lanzó ninguna."
    except ValueError:
        assert True


def test_filter_by_constraints(test_client):
    # Realizar el login
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login fue exitoso."

    # Configurar el payload para la solicitud POST
    payload = {
        "constraints": "5",
        "features": "",
        "models": "",
        "publication_type": "any",
    }

    response = test_client.post("/explore", json=payload)
    assert response.status_code == 200, "La respuesta fue exitosa."

    # Convertir la respuesta JSON a un objeto de Python
    datasets = response.get_json()
    assert datasets is not None, "La respuesta debe contener datos en formato JSON."

    assert len(datasets) == 1, "Debe haber exactamente un dataset en los resultados."


def test_filter_by_constraints_not_result(test_client):
    # Realizar el login
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login fue exitoso."

    # Configurar el payload para la solicitud POST
    payload = {
        "constraints": "123456789",
        "features": "",
        "models": "",
        "publication_type": "any",
    }

    response = test_client.post("/explore", json=payload)
    assert response.status_code == 200, "La respuesta fue exitosa."

    # Convertir la respuesta JSON a un objeto de Python
    datasets = response.get_json()
    assert datasets is not None, "La respuesta debe contener datos en formato JSON."

    assert len(datasets) == 0, "Debe haber cero datasets en los resultados."


def test_filter_by_constraints_wrong_input(test_client):
    # Realizar el login
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login fue exitoso."

    # Configurar el payload para la solicitud POST
    payload = {
        "constraints": "ERRÓNEO",
        "features": "",
        "models": "",
        "publication_type": "any",
    }

    try:
        test_client.post("/explore", json=payload)
        assert False, "Se esperaba una ValueError pero no se lanzó ninguna."
    except ValueError:
        assert True


def test_filter_by_models(test_client):
    # Realizar el login
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login fue exitoso."

    # Configurar el payload para la solicitud POST
    payload = {
        "constraints": "",
        "features": "",
        "models": "1",
        "publication_type": "any",
    }

    response = test_client.post("/explore", json=payload)
    assert response.status_code == 200, "La respuesta fue exitosa."

    # Convertir la respuesta JSON a un objeto de Python
    datasets = response.get_json()
    assert datasets is not None, "La respuesta debe contener datos en formato JSON."

    assert len(datasets) == 1, "Debe haber exactamente un dataset en los resultados."


def test_filter_by_models_no_result(test_client):
    # Realizar el login
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login fue exitoso."

    # Configurar el payload para la solicitud POST
    payload = {
        "constraints": "",
        "features": "",
        "models": "1234567890",
        "publication_type": "any",
    }

    response = test_client.post("/explore", json=payload)
    assert response.status_code == 200, "La respuesta fue exitosa."

    # Convertir la respuesta JSON a un objeto de Python
    datasets = response.get_json()
    assert datasets is not None, "La respuesta debe contener datos en formato JSON."

    assert len(datasets) == 0, "Debe haber cero dataset en los resultados."


def test_filter_by_models_wrong_input(test_client):
    # Realizar el login
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login fue exitoso."

    # Configurar el payload para la solicitud POST
    payload = {
        "constraints": "",
        "features": "",
        "models": "ERRÓNEO",
        "publication_type": "any",
    }

    try:
        test_client.post("/explore", json=payload)
        assert False, "Se esperaba una ValueError pero no se lanzó ninguna."
    except ValueError:
        assert True


def test_filter_by_everything(test_client):
    # Realizar el login
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login fue exitoso."

    # Configurar el payload para la solicitud POST
    payload = {
        "constraints": "5",
        "features": "10",
        "models": "1",
        "publication_type": "any",
    }

    response = test_client.post("/explore", json=payload)
    assert response.status_code == 200, "La respuesta fue exitosa."

    # Convertir la respuesta JSON a un objeto de Python
    datasets = response.get_json()
    assert datasets is not None, "La respuesta debe contener datos en formato JSON."

    assert len(datasets) == 1, "Debe haber exactamente un dataset en los resultados."


def test_filter_by_everything_no_result(test_client):
    # Realizar el login
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login fue exitoso."

    # Configurar el payload para la solicitud POST
    payload = {
        "constraints": "123456789",  # Cambio a constraints para no encontrar ningún dataset
        "features": "10",
        "models": "1",
        "publication_type": "any",
    }

    response = test_client.post("/explore", json=payload)
    assert response.status_code == 200, "La respuesta fue exitosa."

    # Convertir la respuesta JSON a un objeto de Python
    datasets = response.get_json()
    assert datasets is not None, "La respuesta debe contener datos en formato JSON."

    assert len(datasets) == 0, "Debe haber cero datasets en los resultados."
