from django.test.client import Client
from django.core import mail
import test_case_base


class TestAnnouncements(test_case_base.TestCaseBase):
    def setUp(self):

        self.client = Client()
        self.email = 'alice@eatallthecake.com'
        self.password = 'shinyballs'
        self.houseName = 'FunHouse'
        self.zipcode = 98006
        self.createUser(self.email, self.password)
        self.loginUser(self.email, self.password)
        self.createHouse(self.houseName, self.zipcode)

    def test_create_announcement(self):
        '''
        Test create announcement
        '''

        expiration = '2011-01-15'
        text = 'I am testing announcement text'

        # Create announcement
        response = self.client.post(
            '/dashboard/announcement/new/',
            data={'expiration': expiration, 'text': text},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.redirect_chain, []
        )

        mail.outbox = []
        # go to dashboard page
        response = self.client.get('/dashboard/', follow=True)
        self.assertEqual(response.status_code, 200)
        #self.assertContains(response, text, 1)
        #self.assertEqual(1,2)

    #
    # TODO add test for delete announcement
    #
    #
