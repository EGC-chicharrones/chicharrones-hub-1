# Generated by Selenium IDE
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestTestsearchquerys():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_testsearchquerys(self):
        self.driver.get("http://127.0.0.1:5000/")
        self.driver.set_window_size(1050, 731)
        self.driver.find_element(By.LINK_TEXT, "Explore").click()
        self.driver.find_element(By.ID, "query").click()
        self.driver.close()