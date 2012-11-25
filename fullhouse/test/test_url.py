from django.test import TestCase

from django.test.client import Client
#from django.core import mail


## These tests check that expected URLs within the site do exist.
## All pages should be called at least once here to ensure that they
## can be reached.
class TestURLs(TestCase):
    def setUp(self):
        self.client = Client()

    def test_exist_welcome(self):
        response = self.client.get('/welcome/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_exist_dashboard(self):
        response = self.client.get('/dashboard/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_exist_accounts_register(self):
        response = self.client.get('/accounts/register/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_exist_accounts_register_complete(self):
        response = self.client.get('/accounts/register/complete/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_exist_accounts_activate_complete(self):
        response = self.client.get('/accounts/activate/complete/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_exist_accounts_password_reset(self):
        response = self.client.get('/accounts/password/reset/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_exist_accounts_password_reset_done(self):
        response = self.client.get('/accounts/password/reset/done/',
                                   follow=True)
        self.assertEqual(response.status_code, 200)

    def test_exist_accounts_password_reset_complete(self):
        response = self.client.get('/accounts/password/reset/complete/',
                                   follow=True)
        self.assertEqual(response.status_code, 200)

    def test_exist_about_us(self):
        response = self.client.get('/about_us/', follow=True)
        self.assertEqual(response.status_code, 200)
