import pytest

from app import db
from app.modules.conftest import login
from app.modules.auth.models import User
from app.modules.dataset.seeders import DataSetSeeder
from app.modules.dataset.services import DataSetService
from app.modules.profile.models import UserProfile


@pytest.fixture(scope="module")
def test_client(test_app):
    """
    Fixture que inicializa un cliente de pruebas y carga datos iniciales.
    """
    with test_app.app_context():
        # Limpia y configura la base de datos
        db.drop_all()
        db.create_all()

        # Crear usuario y datos necesarios
        user_test = User(email='user@example.com', password='test1234')
        db.session.add(user_test)
        db.session.commit()

        profile = UserProfile(user_id=user_test.id, name="Name", surname="Surname")
        db.session.add(profile)
        db.session.commit()

        # Ejecutar el seeder
        seeder = DataSetSeeder()
        seeder.run()

        # Devuelve el cliente de pruebas
        yield test_app.test_client()

        # Limpieza final
        db.session.remove()
        db.drop_all()


def test_use_existing_dataset(test_client):
    """
    Test que utiliza los datasets creados previamente por el seeder.
    """
    # Autenticar al usuario
    login_response = login(test_client, "user2@example.com", "hashed_password2")
    assert login_response.status_code == 200, "Login was successful."

    # Verifica que el usuario tenga datasets cargados por el seeder
    dataset_service = DataSetService()
    datasets = dataset_service.get_synchronized(User.query.filter_by(email="user2@example.com").first().id)
    dataset_id = dataset_service.latest_synchronized()
    dataset_id = datasets[0].id

    assert dataset_id is not None, "Dataset ID should be present in the response."
    
    # Cambios anonimizar usuario
    response = test_client.post(
        f"/dataset/anonymize/{dataset_id}/",
        follow_redirects=True)

    assert response.status_code == 200, "Anonymize status change was successful."