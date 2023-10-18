from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


class MySeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_home(self):
        self.selenium.get(f"{self.live_server_url}")
