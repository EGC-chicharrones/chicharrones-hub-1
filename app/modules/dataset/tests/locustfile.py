from bs4 import BeautifulSoup
from locust import HttpUser, TaskSet, task
from core.locust.common import get_csrf_token
from core.environment.host import get_host_for_locust_testing

class CombinedBehavior(TaskSet):
    def on_start(self):
        self.view_rating_form()

    @task
    def view_rating_form(self):
        dataset_id = 1
        response = self.client.get(f"/dataset/rate/{dataset_id}/")
        self.csrf_token = get_csrf_token(response)  # Almacenar el token CSRF en una variable de instancia
        print(f"CSRF token obtained: {self.csrf_token}")  # Imprimir el token CSRF

    @task
    def create_rating(self):
        if not hasattr(self, 'csrf_token'):
            print("CSRF token not found. Skipping create_rating task.")
            return

        dataset_id = 1
        data = {
            "csrf_token": self.csrf_token,  # Usar el token CSRF almacenado
            "value": "5",
            "comment": "Great dataset!"
        }
        response = self.client.post(f"/datasets/{dataset_id}/create/rating", data=data)
        if response.status_code != 200:
            print(f"Failed to create rating: {response.status_code}")
        else:
            print("Rating created successfully")

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

class CombinedUser(HttpUser):
    tasks = [CombinedBehavior]
    min_wait = 5000
    max_wait = 9000
    host = get_host_for_locust_testing()