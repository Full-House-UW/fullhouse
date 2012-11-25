from django.test.client import Client
from django.core import mail
import test_case_base

class TestUserSettings(test_case_base.TestCaseBase):
    def setUp(self):
        self.client   = Client()
        self.email    = 'alice@eatallthecake.com'
        self.password = 'shiny'
        self.createUser(self.email, self.password)
        self.loginUser(self.email, self.password)
      
    def test_user_settings(self):
        '''
        Test that user can write and read settings 
        '''
        mail.outbox = []
        # birthday
        response = self.client.post('/dashboard/user_settings/',
            data={'birthday':'1978-09-12'},
            follow=True
        )

        self.assertEqual(response.status_code, 200)

        # get user settings
        response = self.client.get('/dashboard/user_settings/',
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.redirect_chain,[]
        )

        print response                
        self.assertContains(response, '1978-09-12', 1)

        #self.assertEqual(1,2)