# Generated by Selenium IDE
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestEditprofile():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_editprofile(self):
        self.driver.get("http://127.0.0.1:5000/")
        self.driver.set_window_size(1050, 731)
        self.driver.find_element(By.CSS_SELECTOR, ".nav-link:nth-child(1)").click()
        self.driver.find_element(By.ID, "email").click()
        self.driver.find_element(By.ID, "email").send_keys("user1@example.com")
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("1234")
        self.driver.find_element(By.ID, "submit").click()
        self.driver.find_element(By.LINK_TEXT, "Edit profile").click()
        self.driver.find_element(By.ID, "is_developer_checkbox").click()
        self.driver.find_element(By.ID, "submit").click()
        self.driver.find_element(By.ID, "github_username").click()
        self.driver.find_element(By.ID, "github_username").send_keys("chicharrones-lover365")
        self.driver.find_element(By.ID, "submit").click()
        self.driver.find_element(By.LINK_TEXT, "Doe, John").click()
        self.driver.find_element(By.LINK_TEXT, "My profile").click()
        self.driver.find_element(By.LINK_TEXT, "Edit profile").click()
        self.driver.find_element(By.ID, "is_developer_checkbox").click()
        self.driver.find_element(By.ID, "submit").click()
        self.driver.find_element(By.LINK_TEXT, "Doe, John").click()
        self.driver.find_element(By.LINK_TEXT, "My profile").click()
        self.driver.close()
