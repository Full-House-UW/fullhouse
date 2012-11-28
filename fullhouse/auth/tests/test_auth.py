import re

from django.test import TestCase
from django.test.client import Client

from django.core import mail


class TestAuth(TestCase):
    def setUp(self):
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
            'email': 'alice@eatallthecake.com',
            'password1': 'shiny',
            'password2': 'shiny',
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

        with self.settings(
                # use the inmemory mail backend so we can get the activation url
                # from the email
                EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            # registration redirects to dashboard on success
            response = self.client.post(
                '/accounts/register/', follow=True, data=register_data)
        self.assertEqual(
            response.redirect_chain,
            [('http://testserver/accounts/register/complete/', 302)]
        )
        self.assertEqual(response.status_code, 200)

        # now get the activation email and trigger activation
        email = mail.outbox[0]
        match = re.search(r'/accounts/activate/([a-f0-9]{40})/',
                          str(email.message()))
        if not match:
            raise Exception('failed to find key in activation email')
        activation_key = match.group(1)

        response = self.client.get('/accounts/activate/%s/' % activation_key,
                                   follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.redirect_chain,
            [('http://testserver/accounts/activate/complete/', 302)]
        )

        # now login succeeds
        response = self.client.post(
            '/accounts/login/',
            data={'email': 'alice@eatallthecake.com', 'password': 'shiny'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.redirect_chain,
            [('http://testserver/dashboard/', 302)]
        )
