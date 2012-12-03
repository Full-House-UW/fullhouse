from django.test import TestCase
from django.contrib.auth.models import User
from django.core import mail
import re


class TestCaseBase(TestCase):
    '''
    Class provides a few basic functions used extensively with most of the
    test cases.
    '''
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
                EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            # registration redirects to dashboard on success
            response = self.client.post(
                '/accounts/register/',
                data=user_registration_data,
                follow=True,
            )
            self.assertEqual(
                response.redirect_chain,
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
        Login user
        '''
        response = self.client.post(
            '/accounts/login/',
            data={'email': eml, 'password': pwd},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.redirect_chain,
            [('http://testserver/dashboard/', 302)]
        )
        ## find user based on email
        user = User.objects.get(email=eml)
        self.assertEqual(self.client.session['_auth_user_id'], user.pk)

    def logoutUser(self, eml):
        """
        Logout user
        """
        # retrieve the user
        user = User.objects.get(email=eml)
        # log out the user
        self.client.post('/accounts/logout/')
        # ensure the user is not in the session
        self.assertNotIn(user.pk, self.client.session)

    def createHouse(self, housename, zipcode):
        # Create a house
        response = self.client.post(
            '/dashboard/',
            data={'name': housename, 'zip_code': zipcode},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.redirect_chain,
            [('http://testserver/dashboard/add_members/', 302)]
        )
        # read house settings
        response = self.client.get(
            '/dashboard/house_settings/',
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [])
        # check that we can read house settings
        self.assertContains(response, housename, 1)
        self.assertContains(response, zipcode, 1)
