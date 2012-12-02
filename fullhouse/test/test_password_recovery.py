from django.test.client import Client
from django.contrib.auth.models import User
from django.core import mail
import re
import test_case_base


class TestPasswordRecovery(test_case_base.TestCaseBase):

    def setUp(self):

        self.client = Client()
        self.email = 'alice@eatallthecake.com'
        self.password = 'shinyballs'
        self.newpassword = 'tinybubbles'
        self.createUser(self.email, self.password)

    def test_password_recovery(self):
        """
        Function tests user password recovery
        """
        mail.outbox = []
        # post request for password reset
        response = self.client.post(
            '/accounts/password/reset/',
            data={'email': 'alice@eatallthecake.com'},
            follow=True
        )
        # validate response status
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.redirect_chain,
            [('http://testserver/accounts/password/reset/done/', 302)]
        )

        # Read the email received to extract password reset key
        email = mail.outbox[0]
        message = str(email.message())
        match = re.search(r'/accounts/password/reset/confirm/(.+)/',
                          message)
        if not match:
            raise Exception("failed to find key in reset email")

        activation_key = match.group(1)

        response = self.client.post(
            '/accounts/password/reset/confirm/%s/' %
            activation_key,
            data={'new_password1': self.newpassword, 'new_password2': self.newpassword},
            follow=True
        )
        print response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.redirect_chain,
            [('http://testserver/accounts/password/reset/complete/', 302)]
        )

        # retrieve the user
        user = User.objects.get(email=self.email)
        # ensure the user is not logged in
        self.assertNotIn(user.pk, self.client.session)
        self.loginUser(self.email, self.newpassword)
        # ensure the user is now logged in with new password
        self.assertEqual(self.client.session['_auth_user_id'], user.pk)
