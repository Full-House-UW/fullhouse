from django.test.client import Client
from django.core import mail
import test_case_base


class TestCreateHouse(test_case_base.TestCaseBase):
    def setUp(self):

        self.client = Client()
        self.email = 'alice@eatallthecake.com'
        self.password = 'shinyballs'
        self.createUser(self.email, self.password)
        self.loginUser(self.email, self.password)

    def test_create_house(self):
        '''
        Test the user can create a house
        '''
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

        # read house settings
        response = self.client.get('/dashboard/house_settings/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [])

        form = response.context['form']
        print form.is_valid()
        print form.errors

        self.assertContains(response, 'MyHouse', 1)
        self.assertContains(response, '98006', 1)
