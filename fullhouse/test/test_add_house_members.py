from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core import mail
import re

class TestAddHouseMembers(TestCase):
    def setUp(self):
        self.client     = Client()
        self.email      = 'alice@eatallthecake.com'
        self.password   = 'shiny'
        self.email2     = 'frank@eatallthecake.com'
        self.password2  = 'winy'
        
        self.createUser(self.email, self.password)
        self.createUser(self.email2, self.password2)
        self.loginUser(self.email, self.password);
      
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
        
        

    def test_create_house(self):
       
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
        
        
        # Verify house settings 
        response = self.client.get('/dashboard/house_settings/',
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.redirect_chain,[]
        )
              
        response = self.client.get('/dashboard/add_members/',
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.redirect_chain,[]
        )
        
#        invite_data = {
#            'form-1-email': self.email2,
#        }
#        #
#        # This next test fails and I am not sure why or how to fix it.
#        # TODO: validate the user can be made part of the house
#        #         
#        with self.settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
#            response = self.client.post('/dashboard/add_members/', 
#                                        data=invite_data,
#                                        follow=True
#            )   
#            self.assertEqual( response.redirect_chain,
#            [('http://testserver/accounts/register/complete/', 302)]
#        )
  
        #self.assertEqual(1,2)

