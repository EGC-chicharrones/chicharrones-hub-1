from selenium import webdriver
from selenium.webdriver.common.by import By


class TestTestdownloadalldatasetsnologin():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_testdownloadalldatasetsnologin(self):
        self.driver.get("http://localhost:5000/")
        self.driver.set_window_size(1702, 963)
        self.driver.find_element(By.LINK_TEXT, "Download all").click()
