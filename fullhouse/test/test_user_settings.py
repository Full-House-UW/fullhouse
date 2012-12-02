from django.test.client import Client
from django.contrib.auth.models import User
from django.core import mail
import test_case_base


class TestUserSettings(test_case_base.TestCaseBase):

    def setUp(self):
        self.client = Client()
        self.email = 'alice@eatallthecake.com'
        self.password = 'shinyballs'
        self.createUser(self.email, self.password)
        self.loginUser(self.email, self.password)

    def test_user_settings(self):
        '''
        Test that user can write and read settings
        '''
        mail.outbox = []
        # birthday
        first_name = 'bob'
        last_name = 'saget'
        birthday = '09-12-1978'
        response = self.client.post(
            '/dashboard/user_settings/',
            data={
                'birthday': birthday,
                'first_name': first_name,
                'last_name': last_name,
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        user = User.objects.get(id=self.client.session['_auth_user_id'])
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertEqual(user.profile.birthday.strftime('%m-%d-%Y'), birthday)

        # get user settings
        response = self.client.get(
            '/dashboard/user_settings/',
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, birthday, 1)
        self.assertContains(response, first_name, 1)
        self.assertContains(response, last_name, 1)
