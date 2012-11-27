from django.test.client import Client
from django.contrib.auth.models import User
import test_case_base

class TestLoginLogout(test_case_base.TestCaseBase):
    def setUp(self):
        self.client   = Client()
        self.email    = 'alice@eatallthecake.com'
        self.password = 'shiny'
        self.createUser(self.email, self.password)     
        
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