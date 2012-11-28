import datetime
import test_case_base

from django.test.client import Client
from django.contrib.auth.models import User

from fullhouse.dashboard.models import Task, TaskInstance


class TestTasks(test_case_base.TestCaseBase):

    def setUp(self):

        self.client = Client()
        self.email = 'alice@eatallthecake.com'
        self.password = 'shiny'
        self.houseName = 'FunHouse'
        self.zipcode = 98006
        self.createUser(self.email, self.password)
        self.loginUser(self.email, self.password)
        self.createHouse(self.houseName, self.zipcode)

    def test_crud_task(self):

        ##################################
        # test create
        ##################################
        user = User.objects.get(id=self.client.session['_auth_user_id'])
        title = 'Fun Task'
        first_due = '12-23-2013'
        frequency = Task.ONCE

        response = self.client.post(
            '/dashboard/task/new/',
            data={
                'title': title,
                'first_due': first_due,
                'participants': [user.profile.id],
                'frequency': frequency
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.redirect_chain,
            [('http://testserver/dashboard/', 302)]
        )

        self.assertEqual(Task.objects.count(), 1)

        new_task = Task.objects.get(id=1)
        self.assertEqual(new_task.title, title)
        self.assertEqual(new_task.creator, user.profile)
        self.assertEqual(new_task.house, user.profile.house)
        self.assertTrue(new_task.is_active)
        self.assertEqual(new_task.frequency, frequency)

        first = new_task.instances.all()[0]
        # only one participant, should be me
        self.assertEqual(first.assignee, user.profile)
        self.assertEqual(first.due_date.strftime("%m-%d-%Y"), first_due)

        ##################################
        # test edit renaming and changing frequency
        ##################################
        title = 'Not So Fun Task'
        frequency = Task.WEEKLY

        response = self.client.post(
            '/dashboard/task/edit/',
            data={
                'title': title,
                'participants': [user.profile.id],
                'frequency': frequency,
                'id': new_task.id,
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.redirect_chain,
            [('http://testserver/dashboard/', 302)]
        )
        self.assertEqual(Task.objects.count(), 1)

        # refetch the object from db (it was changed)
        new_task = Task.objects.get(id=1)
        self.assertEqual(new_task.title, title)
        self.assertEqual(new_task.frequency, frequency)

        ##################################
        # test delete (discontinue)
        ##################################

        response = self.client.post(
            '/dashboard/task/edit/',
            data={
                'id': new_task.id,
                'discontinue': 'Discontinue',
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.redirect_chain,
            [('http://testserver/dashboard/', 302)]
        )
        # discontinue just marks the task as inactive,
        # does not delete it
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.get(id=1)
        self.assertFalse(task.is_active)

    def test_update_task(self):
        # test complete marks ONCE task as inactive
        # test complete creates correct next instance for each
        # frequency type

        ##################################
        # test complete marks ONCE task as inactive
        ##################################
        user = User.objects.get(id=self.client.session['_auth_user_id'])
        title = 'Fun Task'
        first_due = '12-23-2013'
        frequency = Task.ONCE

        response = self.client.post(
            '/dashboard/task/new/',
            data={
                'title': title,
                'first_due': first_due,
                'participants': [user.profile.id],
                'frequency': frequency
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.redirect_chain,
            [('http://testserver/dashboard/', 302)]
        )

        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(TaskInstance.objects.count(), 1)
        # complete the task instance

        response = self.client.get(
            '/dashboard/task/update/complete/',
            data={
                'id': 1,
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        # default redirect is to dashboard
        self.assertEqual(
            response.redirect_chain,
            [('http://testserver/dashboard/', 302)]
        )
        # verify instance was completed
        instance = TaskInstance.objects.get(id=1)
        self.assertEqual(instance.completed_by, user.profile)
        self.assertEqual(instance.completed_date, datetime.date.today())

        # verify task is now inactive since frequency was ONCE
        task = Task.objects.get(id=1)
        self.assertFalse(task.is_active)

        ##################################
        # test complete creates correct next instance for repeated tasks
        ##################################

        timedeltas = {
            Task.DAILY: datetime.timedelta(days=1),
            Task.WEEKLY: datetime.timedelta(weeks=1),
            Task.MONTHLY: datetime.timedelta(days=30),
            Task.YEARLY: datetime.timedelta(weeks=52),
        }
        repeating_frequencies = Task.FREQUENCY_CHOICES[1:]
        for frequency, display in repeating_frequencies:

            title = 'do this %s' % display
            first_due = '12-23-2013'

            response = self.client.post(
                '/dashboard/task/new/',
                data={
                    'title': title,
                    'first_due': first_due,
                    'participants': [user.profile.id],
                    'frequency': frequency
                },
                follow=True
            )
            task = Task.objects.get(title=title)

            response = self.client.get(
                '/dashboard/task/update/complete/',
                data={
                    'id': task.instances.all()[0].id,
                },
                follow=True
            )
            self.assertEqual(response.status_code, 200)
            # default redirect is to dashboard
            self.assertEqual(
                response.redirect_chain,
                [('http://testserver/dashboard/', 302)]
            )
            self.assertEqual(task.instances.count(), 2)
            instances = task.instances.order_by('-due_date')
            # verify old instance is complete
            old = instances[1]
            self.assertEqual(old.completed_by, user.profile)
            self.assertEqual(old.completed_date, datetime.date.today())
            # verify new instance created with correct due_date
            new = instances[0]
            self.assertIsNone(new.completed_by)
            # TODO: test exact timedelta, for now just make sure it's due later
            self.assertTrue(
                new.due_date == task.first_due + timedeltas[frequency]
            )

    def test_history(self):
        # TODO: test history displays expected for basic cases
        pass
