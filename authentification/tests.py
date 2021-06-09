from django.test import TestCase
from decouple import config
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from substitution.constants import LOG_IN_OK
# import logging


class MySeleniumTests(StaticLiveServerTestCase):
    fixtures = ['users.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        timeout = 2
        self.selenium.get('{}'.format(self.live_server_url + '/signin'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(config('USER_LOGIN'))
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(config('USER_PWD'))
        password_input.send_keys(Keys.RETURN)
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name('body'))
        login = False
        if LOG_IN_OK in self.selenium.page_source:
            login = True
        assert login is True
