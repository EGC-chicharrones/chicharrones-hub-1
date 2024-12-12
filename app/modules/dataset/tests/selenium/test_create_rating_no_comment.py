# Generated by Selenium IDE
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestCreateratingnocomment():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_createratingnocomment(self):
        self.driver.get("http://192.168.159.127:5000/")
        self.driver.set_window_size(1050, 699)
        self.driver.find_element(By.LINK_TEXT, "Ratings").click()
        self.driver.find_element(By.ID, "email").click()
        self.driver.find_element(By.ID, "email").send_keys("user1@example.com")
        self.driver.find_element(By.CSS_SELECTOR, ".row:nth-child(3) > .col-md-6").click()
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("1234")
        self.driver.find_element(By.ID, "submit").click()
        self.driver.find_element(By.LINK_TEXT, "Ratings").click()
        self.driver.find_element(By.CSS_SELECTOR, ".star:nth-child(3)").click()
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
        self.driver.find_element(By.CSS_SELECTOR, ".text-dark").click()
        self.driver.find_element(By.CSS_SELECTOR, ".dropdown-item:nth-child(2)").click()
        self.driver.close()
