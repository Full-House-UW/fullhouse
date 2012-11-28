from django.test.client import Client
from django.core import mail
import test_case_base


class TestAddHouseMembers(test_case_base.TestCaseBase):
    def setUp(self):
        self.client = Client()
        self.email = 'alice@eatallthecake.com'
        self.password = 'shiny'
        self.email2 = 'frank@eatallthecake.com'
        self.password2 = 'winy'

        self.createUser(self.email, self.password)
        self.createUser(self.email2, self.password2)
        self.loginUser(self.email, self.password)

    def test_create_house(self):

        mail.outbox = []
        # go to dashboard page
        response = self.client.post('/dashboard/', follow=True)

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
        response = self.client.get('/dashboard/house_settings/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [])

        response = self.client.get('/dashboard/add_members/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [])
