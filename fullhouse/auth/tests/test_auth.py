import re

from django.test import TestCase
from django.test.client import Client

from django.core import mail

from fullhouse.test.test_case_base import TestCaseBase


class TestAuth(TestCaseBase):
    def setUp(self):
        self.email = 'alice@eatallthecake.com'
        self.password = 'shinyballs'
        self.client = Client()

    def testUnauthenticatedRedirect(self):
        response = self.client.get('/dashboard/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.redirect_chain,
            [('http://testserver/accounts/login/?next=/dashboard/', 302)]
        )

    def testRegistration(self):
        register_data = {
            'email': self.email,
            'password1': self.password,
            'password2': self.password,
        }

        # first attempt at login fails
        response = self.client.post(
            '/accounts/login/',
            data={'email': 'alice@eatallthecake.com', 'password': 'nope'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.redirect_chain,
            []
        )

        # create user
        self.createUser(self.email, self.password)

        # now login succeeds
        self.loginUser(self.email, self.password)

        # login page redirects to dashboard
        response = self.client.get(
            '/accounts/login/',
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.redirect_chain,
            [('http://testserver/dashboard/', 302)]
        )
        # registration page redirects to dashboard
        response = self.client.get(
            '/accounts/register/',
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.redirect_chain,
            [('http://testserver/dashboard/', 302)]
        )
