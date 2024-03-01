""" These tests follow user stories and test the system from the user's perspective with a real browser. """

import logging

from django.conf import settings
from django.contrib.auth.models import Group, User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)


class SeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.browser_version = 120
        options.add_argument("--no-sandbox")
        options.add_argument(
            "--headless=new"
        )  # https://www.selenium.dev/blog/2023/headless-is-going-away/

        cls.test_username = "testuser"
        cls.test_email = "testuser@email.com"
        cls.test_password = "testpassword"

        cls.test_staff_username = "teststaffuser"
        cls.test_staff_email = "teststaffuser@email.com"
        cls.test_staff_password = "teststaffpassword"

        cls.test_admin_username = "testadminuser"
        cls.test_admin_email = "testadminuser@email.com"
        cls.test_admin_password = "testadminpassword"

        cls.selenium = webdriver.Chrome(options=options)

        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def create_test_user(self):
        self.user = User.objects.create_user(
            username=self.test_username,
            email=self.test_email,
            password=self.test_password,
        )

    def create_test_staff_user(self):
        self.staff_user = User.objects.create_user(
            username=self.test_staff_username,
            email=self.test_staff_email,
            password=self.test_staff_password,
            is_staff=True,
        )

    def create_test_superuser(self):
        self.super_user = User.objects.create_user(
            username=self.test_admin_username,
            email=self.test_admin_email,
            password=self.test_admin_password,
            is_staff=True,
            is_superuser=True,
        )

    def create_groups(self):
        for group in settings.DJANGO_GROUPS:
            Group.objects.create(name=group)

    def test_homepage(self):
        self.create_groups()
        self.create_test_user()
        self.assertTrue(User.objects.filter(username=self.test_username).exists())

        # A user browses to the home page
        self.selenium.get(f"{self.live_server_url}")

        # They see the system logo
        system_logo_selector = (
            '//img[@alt="Department of Parks and Wildlife - Prescribed Burns System"]'
        )
        self.assertTrue(
            self.selenium.find_element(By.XPATH, system_logo_selector).is_displayed()
        )

        # They see the navigation bar
        navbar = self.selenium.find_element(By.CLASS_NAME, "navbar")
        self.assertTrue(navbar.is_displayed())

        # They see the correct elements in the navigation bar
        nav_links = navbar.find_elements(By.CLASS_NAME, "nav-link")

        # there is one nav link
        self.assertEqual(len(nav_links), 1)

        home_link = nav_links[0]

        # The nav link text is 'Home'
        self.assertEqual(home_link.get_attribute("innerText"), "Home")

        login_button_selector = '//a[@href="/ssologin"]'
        login_button = self.selenium.find_element(By.XPATH, login_button_selector)

        if not login_button.is_displayed():
            # They don't see the login button
            navbar_toggler = self.selenium.find_element(By.CLASS_NAME, "navbar-toggler")
            # They see the navbar toggler
            if navbar_toggler.is_displayed():
                # They click the navbar toggler
                navbar_toggler.click()
            else:
                raise Exception("Navbar toggler is not visible")

        self.selenium.implicitly_wait(3)

        # The login button is enabled
        if not login_button.is_enabled():
            raise Exception("Login button is not enabled")

        # They click the login button
        login_button.click()
        self.selenium.implicitly_wait(5)

        # They are redirected to the login page
        login_form = self.selenium.find_element(By.CLASS_NAME, "login-form")

        # They see a login form
        self.assertTrue(login_form.is_displayed())

        # They see a username field
        username_field = self.selenium.find_element(By.ID, "id_username")

        # They see a password field
        password_field = self.selenium.find_element(By.ID, "id_password")

        # They see a login button
        login_button = login_form.find_element(By.TAG_NAME, "button")
        self.assertEqual(
            login_button.get_attribute("innerText").strip().lower(), "login"
        )

        # They enter their username
        username_field.send_keys(self.test_username)

        # They enter their password
        password_field.send_keys(self.test_password)

        self.selenium.implicitly_wait(3)

        # They click the login button
        login_button.click()

        # They are redirected to the home page
        self.selenium.implicitly_wait(3)

        # They see the navigation bar
        navbars = self.selenium.find_elements(By.CLASS_NAME, "navbar")

        for navbar in navbars:
            self.assertTrue(navbar.is_displayed())

        # They see the correct elements in the navigation bar
        nav_links_text = [
            "Home",
            "Burn Planning",
            "Operational Planning",
            "Implementation",
            "Treatment",
            "Aviation",
            "Search",
        ]
        nav_links = navbars[1].find_elements(By.CLASS_NAME, "nav-link")
        for nav_link in nav_links:
            self.assertIn(nav_link.get_attribute("innerText"), nav_links_text)
            # Just quick way to ignore the other nav links for not TODO: make more robust
            if nav_link.get_attribute("innerText") == "Search":
                break

    def test_admin_login(self):
        self.create_test_superuser()
        path = reverse("admin:index")

        # A superuser navigates to the django admin index page
        self.selenium.get(f"{self.live_server_url}{path}")
        login_form = self.selenium.find_element(By.ID, "login-form")

        if not login_form.is_displayed():
            raise Exception("Login form is not visible")

        # They are redirected to the login page
        login_form = self.selenium.find_element(By.ID, "login-form")

        # They see a login form
        self.assertTrue(login_form.is_displayed())

        # They see a username field
        username_field = self.selenium.find_element(By.ID, "id_username")

        # They see a password field
        password_field = self.selenium.find_element(By.ID, "id_password")

        # They see a login button
        login_button = login_form.find_element(By.XPATH, '//input[@type="submit"]')
        self.assertEqual(login_button.get_attribute("value").strip().lower(), "log in")

        # They enter their username
        username_field.send_keys(self.test_admin_username)

        # They enter their password
        password_field.send_keys(self.test_admin_password)

        self.selenium.implicitly_wait(3)

        # They click the login button
        login_button.click()
