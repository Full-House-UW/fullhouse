from django.test.client import Client
import test_case_base


class TestPasswordChange(test_case_base.TestCaseBase):
    def setUp(self):

        self.client = Client()
        self.email = 'alice@eatallthecake.com'
        self.password = 'shinyballs'
        self.newpassword = 'tinybubbles'
        self.createUser(self.email, self.password)
        self.loginUser(self.email, self.password)

    def test_password_change(self):

        # Write out a new password
        response = self.client.post(
            '/accounts/password/change/',
            data={
                'old_password': self.password,
                'new_password1': self.newpassword,
                'new_password2': self.newpassword,
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.redirect_chain,
            [('http://testserver/accounts/password/change/done/', 302)]
        )

        # logout user
        self.logoutUser(self.email)
        # login use with new password
        self.loginUser(self.email, self.newpassword)
