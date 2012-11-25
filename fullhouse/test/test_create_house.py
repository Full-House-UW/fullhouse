from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core import mail
import re


class TestCreateHouse(TestCase):
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

        # now login  user
        response = self.client.post(
            '/accounts/login/',
            data={'email': self.email, 'password': self.password},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.redirect_chain,
            [('http://testserver/dashboard/', 302)]
        )
        
        user = User.objects.get(email=self.email)
        # ensure the user is logged in 
        self.assertEqual(self.client.session['_auth_user_id'], user.pk)
        
    def test_create_house(self):
        '''
        Test the user can create a house
        '''
        mail.outbox = []
        # go to dashboard page 
        response = self.client.post('/dashboard/',
            follow=True
        )
        
        self.assertEqual(response.status_code, 200)
        
        # Create a house
        response = self.client.post(
            '/dashboard/',
            data={'name': 'MyHouse', 'zip_code': '98006'},
            follow=True
        )
        
        #print response
        self.assertEqual(
            response.redirect_chain, 
            [('http://testserver/dashboard/add_members/', 302)]
        )
        
        
        # read house settings
        response = self.client.get('/dashboard/house_settings/',
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.redirect_chain,[]
        )

        form = response.context['form']
        print form.is_valid()
        print form.errors
                
        self.assertContains(response, 'MyHouse', 1)
        self.assertContains(response, '98006', 1)

        #self.assertEqual(1,2)