# Generated by Selenium IDE
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestSeleniumtestmodelsfilter():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_seleniumtestmodelsfilter(self):
        self.driver.get("http://127.0.0.1:5000/")
        self.driver.set_window_size(1854, 1048)
        element = WebDriverWait(self.driver, 10).until(
          EC.element_to_be_clickable((By.CSS_SELECTOR, ".sidebar-item:nth-child(3) .align-middle:nth-child(2)")))
        element.click()
        models_input = self.driver.find_element(By.ID, "models")
        for i in range(1, 11):
            models_input.clear()
            models_input.send_keys(str(i))
            time.sleep(0.4)
        self.driver.close()
