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


class DatasetUser(HttpUser):
    tasks = [DatasetBehavior]
    min_wait = 5000
    max_wait = 9000
    host = get_host_for_locust_testing()
