from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core import mail
import re

class TestLoginLogout(TestCase):
    def setUp(self):
        self.client   = Client()
        self.email    = 'alice@eatallthecake.com'
        self.password = 'shiny'
      
        user_registration_data = {
            'email': self.email,
            'password1': self.password,
            'password2': self.password,
        }
      
        # register user alice 
        with self.settings(
            EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'
            ):
            # registration redirects to dashboard on success
            response = self.client.post('/accounts/register/', follow=True,
                data=user_registration_data)
            self.assertEqual( response.redirect_chain,
            [('http://testserver/accounts/register/complete/', 302)]
        )
        self.assertEqual(response.status_code, 200)


        # now get the activation email and trigger activation for the 
        # user
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
      
        
    def test_log_in_user(self):
        """
        Verify the user can login
        """
        response = self.client.post('/accounts/login/',
            data={'email': 'alice@eatallthecake.com', 'password': 'shiny'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.redirect_chain,
            [('http://testserver/dashboard/', 302)]
        )
        user = User.objects.get(email='alice@eatallthecake.com')
        self.assertEqual(self.client.session['_auth_user_id'], user.pk)
        
    def test_log_out_user(self):
        """
        Verify that user can be logged out
        """
        response = self.client.post('/accounts/login/',
            data={'email': 'alice@eatallthecake.com', 'password': 'shiny'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.redirect_chain,
            [('http://testserver/dashboard/', 302)]
        )
        # retrieve the user 
        user = User.objects.get(email='alice@eatallthecake.com')
        # ensure the user is in session 
        self.assertEqual(self.client.session['_auth_user_id'], user.pk)
        # log out the user
        response = self.client.post('/accounts/logout/')
        # ensure the user is not in the session 
        self.assertNotIn(user.pk, self.client.session)