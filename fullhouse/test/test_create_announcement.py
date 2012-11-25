from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core import mail
import re


class TestCreateAnnouncement(TestCase):
    def setUp(self):

        self.client   = Client()
        self.email    = 'alice@eatallthecake.com'
        self.password = 'shiny' 
        self.houseName = 'FunHouse'
        self.zipcode = 98006
        self.createUser(self.email,  self.password);
        self.loginUser(self.email, self.password)
        self.createHouse(self.houseName, self.zipcode)
      
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
        
    def createHouse(self, housename, zipcode):
        # Create a house
        response = self.client.post('/dashboard/',
                                    data={'name': housename, 'zip_code': zipcode},
                                    follow=True
        )
        self.assertEqual(response.status_code, 200)
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
        # check that we can read house settings
        self.assertContains(response, housename, 1)
        self.assertContains(response, zipcode, 1)
        
        
    def test_create_announcement(self):
        '''
        Test create announcement 
        '''
        ##
        expiration = '2011-01-15'
        text = 'I am testing announcement text'


        # Create announcement
        response = self.client.post('/dashboard/announcement/new/',
                                    data={'expiration': expiration, 'text': text},
                                    follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.redirect_chain, [('http://testserver/dashboard/', 302)]
        )
        
        mail.outbox = []
        # go to dashboard page 
        response = self.client.get('/dashboard/',
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        #self.assertContains(response, text, 1)
        #self.assertEqual(1,2)
     
    #    
    # TODO add test for delete announcement 
    #
    # 