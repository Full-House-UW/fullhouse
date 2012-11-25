from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core import mail
import re

class TestPasswordRecovery(TestCase):
    def setUp(self):
      
        self.client   = Client()
        self.email    = 'alice@eatallthecake.com'
        self.password = 'shiny'
        self.newpassword = 'tiny'
        self.createUser(self.email, self.password)

    def createUser(self, email, password):
        '''
        Utility function creates a new user with given  email and pwd
        '''
        # clear email client 
        mail.outbox = []
        
        # Create registration data
        user_registration_data = {
            'email': email,
            'password1': password,
            'password2': password,
        }
      
        # register user
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
        
    def loginUser(self, eml, pwd):
        '''
        Function logs in the given user
        '''
        response = self.client.post('/accounts/login/',
            data={'email': eml, 'password': pwd},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.redirect_chain,
            [('http://testserver/dashboard/', 302)]
        )
        ## find user based on email 
        user = User.objects.get(email = eml)
        self.assertEqual(self.client.session['_auth_user_id'], user.pk)
        
        

    def test_password_recovery(self):
        """
        Function tests user password recovery
        """
        mail.outbox = []
        # post request for password reset
        response = self.client.post('/accounts/password/reset/',
            data={'email': 'alice@eatallthecake.com'},
            follow=True
        )
        # validate response status 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.redirect_chain,
            [('http://testserver/accounts/password/reset/done/', 302)]
        )

        # Read the email received to extract password reset key
        email = mail.outbox[0]
        message = str(email.message())
        match = re.search(r'/accounts/password/reset/confirm/(.+)/',
                          message)
        if not match:
            raise Exception("failed to find key in reset email")

        activation_key = match.group(1)

        response = self.client.post('/accounts/password/reset/confirm/%s/' %
            activation_key,
            data={'new_password1': self.newpassword, 'new_password2': self.newpassword},
            follow=True
        )
        print response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.redirect_chain,
            [('http://testserver/accounts/password/reset/complete/', 302)]
        )

        # retrieve the user 
        user = User.objects.get(email=self.email)
        # ensure the user is not logged in  
        self.assertNotIn(user.pk, self.client.session)
        self.loginUser(self.email, self.newpassword)
        # ensure the user is now logged in with new password
        self.assertEqual(self.client.session['_auth_user_id'], user.pk)

