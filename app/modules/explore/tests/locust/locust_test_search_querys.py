from locust import HttpUser, TaskSet, task
from core.environment.host import get_host_for_locust_testing


class ExploreBehavior(TaskSet):
    def on_start(self):
        self.explore_page()

    @task
    def explore_page(self):
        """
        Test for accessing the explore page (GET request).
        """
        response = self.client.get("/explore")
        if response.status_code != 200:
            print(f"Failed to load Explore page: {response.status_code}")
        else:
            print("Explore page loaded successfully")

    @task
    def explore_search(self):
        """
        Test for performing a search query on the explore page (POST request).
        """
        search_payload = {
            "query": "author:John Doe;tags:AI"
        }
        response = self.client.post("/explore", json=search_payload)
        if response.status_code != 200:
            print(f"Failed to perform search: {response.status_code}")
        else:
            print(f"Search performed successfully: {response.json()}")

    @task
    def explore_invalid_search(self):
        """
        Test for handling invalid search queries.
        """
        search_payload = {
            "query": "invalid_filter:invalid_value"
        }
        response = self.client.post("/explore", json=search_payload)
        if response.status_code != 200:
            print(f"Failed to handle invalid search: {response.status_code}")
        else:
            print(f"Handled invalid search: {response.json()}")


class ExploreUser(HttpUser):
    tasks = [ExploreBehavior]
    min_wait = 3000  # Minimum wait time in milliseconds
    max_wait = 7000  # Maximum wait time in milliseconds
    host = get_host_for_locust_testing()