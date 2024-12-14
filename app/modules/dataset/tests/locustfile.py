from locust import HttpUser, TaskSet, task
from core.locust.common import get_csrf_token
from core.environment.host import get_host_for_locust_testing


class DatasetBehavior(TaskSet):
    def on_start(self):
        self.dataset()

    @task
    def dataset(self):
        response = self.client.get("/dataset/upload")
        get_csrf_token(response)

    @task
    def change_anonymize_unsync(self):
        dataset_id = 1
        response = self.client.get(f"/dataset/anonymize/unsync/{dataset_id}/")
        csrf_token = get_csrf_token(response)

        response = self.client.post(f"/dataset/anonymize/unsync/{dataset_id}/", data={
            "csrf_token": csrf_token
        })
        if response.status_code != 200:
            print(f"Failed to change anonymize (unsync): {response.status_code}")
        else:
            print("Change anonymize (unsync) successful")

    @task
    def change_anonymize_sync(self):
        dataset_id = 1

        response = self.client.get(f"/dataset/anonymize/{dataset_id}/")
        csrf_token = get_csrf_token(response)

        response = self.client.post(f"/dataset/anonymize/{dataset_id}/", data={
            "csrf_token": csrf_token
        })
        if response.status_code != 200:
            print(f"Failed to change anonymize (sync): {response.status_code}")
        else:
            print("Change anonymize (sync) successful")

    @task
    def test_download_all_datasets(self):
        """
        Test de carga para /dataset/download/all.
        """
        response = self.client.get("/dataset/download/all")
        if response.status_code == 200:
            print("Download all datasets successful.")
        else:
            print(f"Failed to download datasets: {response.status_code}")

    @task
    def test_view_rating_form(self):
        """
        Test para ver el formulario de calificación y las calificaciones de un dataset.
        """
        dataset_id = 1  # Cambia esto al ID real del dataset que quieras probar
        response = self.client.get(f"/dataset/rate/{dataset_id}/")

        if response.status_code == 200:
            print(f"Successfully retrieved rating form for dataset {dataset_id}.")
        else:
            print(f"Failed to retrieve rating form for dataset {dataset_id}: {response.status_code}")

        if 'form' in response.text:
            print("Rating form is present in the response.")
        else:
            print("Rating form is missing in the response.")

        if 'ratings' in response.text:
            print("Ratings are present in the response.")
        else:
            print("Ratings are missing in the response.")

    @task
    def test_create_rating(self):
        """
        Test para la creación de una calificación en un dataset.
        """

        dataset_id = 1

        response = self.client.get(f"/datasets/{dataset_id}/create/rating")

        if response.status_code == 200:
            print(f"Successfully retrieved rating creation form for dataset {dataset_id}.")
        else:
            print(f"Failed to retrieve rating creation form for dataset {dataset_id}: {response.status_code}")
            return

        rating_value = 4
        comment = "Excelente dataset, muy útil."

        data = {
            "value": rating_value,
            "comment": comment
        }

        csrf_token = get_csrf_token(response)
        data['csrf_token'] = csrf_token

        response = self.client.post(f"/datasets/{dataset_id}/create/rating", data=data)

        if response.status_code == 302:
            print(f"Successfully created rating for dataset {dataset_id}.")
            print(f"Redirected to: {response.headers['Location']}")
        else:
            print(f"Failed to create rating for dataset {dataset_id}: {response.status_code}")

        if 'Valoración creada con éxito' in response.text:
            print("Rating creation was successful, flash message received.")
        else:
            print("Rating creation failed or flash message not received.")


class DatasetUser(HttpUser):
    tasks = [DatasetBehavior]
    min_wait = 5000
    max_wait = 9000
    host = get_host_for_locust_testing()
