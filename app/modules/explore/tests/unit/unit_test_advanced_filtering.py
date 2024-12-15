import pytest
from app import db
from app.modules.dataset.models import DataSet, DSMetaData, PublicationType
from app.modules.featuremodel.models import FeatureModel


@pytest.fixture(scope="module")
def test_client_with_data(test_client):
    with test_client.application.app_context():
        # Crear dataset y metadatos
        ds_meta_data = DSMetaData(
            title="Test Dataset",
            description="Dataset for testing filters",
            publication_type=PublicationType.DATA_MANAGEMENT_PLAN,
            tags="test, dataset"
        )
        db.session.add(ds_meta_data)

        dataset = DataSet(user_id=1, ds_meta_data=ds_meta_data)
        db.session.add(dataset)
        db.session.flush()  # Generar ID del dataset

        for i in range(3):
            feature_model = FeatureModel(data_set_id=dataset.id, features=10 * (i + 1), constraints=5 * (i + 1))
            db.session.add(feature_model)

        db.session.commit()

    yield test_client


'''def test_filter_by_models(test_client):
    # Realizar el login
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login fue exitoso."

    # Configurar el payload para la solicitud POST
    payload = {
        "constraints": "",
        "features": "10",
        "models": "",
        "publication_type": "any",
        "query": "",
        "sorting": "newest",
    }

    response = test_client.post("/explore", json=payload)
    assert response.status_code == 200, "La respuesta fue exitosa."

    # Convertir la respuesta JSON a un objeto de Python
    datasets = response.get_json()
    assert datasets is not None, "La respuesta debe contener datos en formato JSON."

    assert len(datasets) == 1, "Debe haber exactamente un dataset en los resultados."'''
