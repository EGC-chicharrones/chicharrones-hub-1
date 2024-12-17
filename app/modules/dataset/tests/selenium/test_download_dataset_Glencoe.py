# Generated by Selenium IDE
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestDownloaddatasetGlencoe():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_downloaddatasetGlencoe(self):
        self.driver.get("http://127.0.0.1:5000/")
        self.driver.maximize_window()
        self.driver.find_element(By.LINK_TEXT, "Sample dataset 4").click()
        self.driver.find_element(By.ID, "btnGroupDropDownload4").click()
        self.driver.find_element(By.LINK_TEXT, "Glencoe").click()
