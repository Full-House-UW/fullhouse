import datetime
import hashlib
import random
import pdb

from django.conf import settings
from django.core.mail import send_mail
from django.core.validators import *
from django.contrib.auth.models import User
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site

from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

try:
    from django.utils.timezone import now as datetime_now
except ImportError:
    datetime_now = datetime.datetime.now

from registration.models import SHA1_RE

import logging

logger = logging.getLogger(__name__)

# Notes:
# - Django automatically creates an 'id' field as a primary key
# - I've created alright __str__ methods, but feel free to change them to
#   suit you
# - Because we use the related_name argument when defining foreign keys, you
#   can access UserProfiles and Announcements through House objects.
#   For example:
#   h = House.objects.get(name='my house')
#   h.members.all()
#   This lists all of the members of the given house.


class House(models.Model):
    name = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=9, validators=[RegexValidator(regex=r'^[0-9]{5}$', message="Please enter a 5 digit zip code.")], null=True, blank=True)

    def __str__(self):
        return self.name


class InviteManager(models.Manager):

    def is_valid(self, user, invite_key):
        """
        TODO: documentation
        """
        if SHA1_RE.search(invite_key):
            try:
              invite = self.get(invite_key=invite_key)
            except self.model.DoesNotExist:
              return False
            return not invite.invite_key_expired() and user.email == invite.email
        return False

    def accept_invite(self, user, invite_key):
        """
        TODO: documentation
        """
        if SHA1_RE.search(invite_key):
            try:
                invite = self.get(invite_key=invite_key)
            except self.model.DoesNotExist:
                return False
            if not invite.invite_key_expired() and user.email == invite.email:
                profile = user.profile
                profile.house = invite.house
                profile.save()
                invite.invite_key = self.model.INVITE_ACCEPTED
                invite.save()
                return user
        return False

    def create_member_invite(self, email, from_user, house):
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        housename = house.name
        if isinstance(email, unicode):
            housename = housename.encode('utf-8')
        if isinstance(email, unicode):
            email = email.encode('utf-8')

        invite_key = hashlib.sha1(salt + email + housename).hexdigest()
        invite_profile = self.create(
            house=house,
            email=email,
            invite_key=invite_key,
            sent_date=datetime_now()
        )

        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        invite_profile.send_invite_email(site, from_user)

        return invite_profile

    def delete_expired_invites(self):
        for profile in self.all():
            if profile.invite_key_expired():
                profile.delete()


class InviteProfile(models.Model):

    INVITE_ACCEPTED = u"ALREADY_ACCEPTED"

    house = models.ForeignKey(House, related_name='invitees')
    email = models.EmailField()
    invite_key = models.CharField(_('house invite key'), max_length=40)
    sent_date = models.DateTimeField()

    objects = InviteManager()

    def invite_key_expired(self):
        expiration_date = datetime.timedelta(
            days=settings.INVITE_ACTIVATION_DAYS
        )
        return self.invite_key == self.INVITE_ACCEPTED or \
            (self.sent_date + expiration_date <= datetime_now())

    def send_invite_email(self, site, from_user):
        ctx_dict = {'invite_key': self.invite_key,
                    'expiration_days': settings.INVITE_ACTIVATION_DAYS,
                    'from_username': from_user.username,
                    'housename': self.house.name,
                    'site': site}
        subject = render_to_string('addmembers/invite_email_subject.txt',
                                   ctx_dict)
        subject = ''.join(subject.splitlines())
        message = render_to_string('addmembers/invite_email.txt',
                                   ctx_dict)

        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        from_email = settings.DEFAULT_FROM_EMAIL

        send_mail(subject, message, from_email, (self.email,))

    def __str__(self):
        return self.email


class UserProfile(models.Model):

    MALE = 'mm'
    FEMALE = 'ff'
    # There's a pc issue here, but
    # we allow the gender to be blank
    GENDER_CHOICES = (
        (MALE, 'male'),
        (FEMALE, 'female'),
    )

    user = models.OneToOneField(User, related_name='profile')
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=4, choices=GENDER_CHOICES, null=True, blank=True
    )
    # should perhaps be a ManyToManyField, but for simplicity, we'll only allow
    # one house per person for now.
    house = models.ForeignKey(
        House, related_name='members', null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        if self.user.first_name or self.user.last_name:
            return self.user.first_name + " " + self.user.last_name + " <" + self.user.email + ">"
        else:
            return self.user.email


class Announcement(models.Model):
    creator = models.ForeignKey(UserProfile)
    text = models.TextField()
    house = models.ForeignKey(House, related_name='announcements')
    expiration = models.DateField(null=True)

    def __str__(self):
        return "%s: %s" % (self.creator, self.text)

    class Meta:
        ordering = ['-id']


class TaskManager(models.Manager):

    def create_task(self, creator, task_form):
        """
        Create a new ``Task`` and a ``TaskInstance`` due at the task's
        first_due date.

        `creator` - ``UserProfile`` of the task's creator

        `create_task_form` - bound and verified ``CreateTaskForm`` with data
            for new task

        """

        assert task_form.is_valid()

        task = task_form.save(commit=False)
        task.creator = creator
        task.house = creator.house
        task.is_active = True
        task.save()
        #need to save many to many data
        task_form.save_m2m()

        current = TaskInstance.objects.create(
            task=task,
            #random first assignee
            assignee=random.choice(task.participants.all()),
            due_date=task.first_due,
        )
        current.save()

    def update_taskinstance(self, t_id, userprofile, action):
        """
        Update TaskInstance with given id. No-op if the taskinstance
        does not exist, or if the user associated with given userprofile
        is not a participant in the task.
        Repeated calls to this function with the same parameters will
        not change models from their state after the first call.

        """

        try:
            instance = TaskInstance.objects.get(id=t_id)
        except TaskInstance.DoesNotExist:
            return
        if userprofile not in instance.task.participants.all():
            return
        if action == 'complete':
            if instance.completed_by is not None:
                return
            instance.complete(userprofile)
            instance.save()
            if instance.task.frequency == Task.ONCE:
                instance.task.is_active = False
                instance.task.save()
            else:
                new = instance.create_next()
                if new is not None:
                    new.save()

    def _get_updated_task_instances(self, task):
        """
        Return tuple (current, previous) of updated task instances
        for the given task.

        Postcondition: task has at least 1 instance:
            current instance (today <= due_date < today+frequency)

        """
        instances = task.instances.order_by('-due_date')[:2]
        # note len() fetches the objects, but we need them anyway
        num_instances = len(instances)
        if num_instances == 2:
            # we have a current and a previous
            current = instances[0]
            prev = instances[1]
        elif num_instances == 1:
            # new instance, only current created
            current = instances[0]
            prev = None
        else:
            logger.error('Missing task instance for task_id %d' % task.id)
            current = TaskInstance.objects.create(
                task=task,
                #random first assignee
                assignee=random.choice(task.participants.all()),
                due_date=task.first_due
            )
            current.save()
            prev = None

        return (current, prev)

    def get_house_task_list(self, house):
        """
        Return list of task data for each of the given house's active tasks.

        """

        tasks = []
        for task in house.tasks.all():
            if not task.is_active:
                continue
            current, prev = self._get_updated_task_instances(task)
            t = {
                'title': task.title,
                'description': task.description,
                'frequency': task.get_frequency_display(),
                'creator': task.creator,
                'participants': task.participants.all(),
                'id': task.id,
                'current': current,
                'prev': prev,
            }
            if current.due_date < datetime.date.today():
                t['overdue'] = True
            tasks.append(t)

        return tasks

    def get_task_history(self, house):
        tasks = []
        for task in house.tasks.all():
            t = {
                'title': task.title,
                'id': task.id,
                'instances': task.instances.all(),
                'participants': task.participants.all(),
            }
            tasks.append(t)

        return tasks


class Task(models.Model):
    """
    Represents a task definition
    """

    ONCE = '--'
    DAILY = 'DD'
    WEEKLY = 'WW'
    MONTHLY = 'MM'
    YEARLY = 'YY'
    FREQUENCY_CHOICES = (
        (ONCE, 'once'),
        (DAILY, 'daily'),
        (WEEKLY, 'weekly'),
        (MONTHLY, 'monthly'),
        (YEARLY, 'yearly'),
    )

    objects = TaskManager()

    house = models.ForeignKey(House, related_name='tasks')
    creator = models.ForeignKey(UserProfile, related_name='tasks_created')
    is_active = models.BooleanField(default=False)

    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    frequency = models.CharField(
        max_length=4, choices=FREQUENCY_CHOICES, default=ONCE
    )
    participants = models.ManyToManyField(
        UserProfile, related_name='tasks_participating'
    )
    first_due = models.DateField()

    def __str__(self):
        return "%s: %s" % (str(self.creator), self.title)


class TaskInstance(models.Model):
    """
    Represents a single instance of a (possibly recurring) task
    """

    task = models.ForeignKey(Task, related_name='instances')
    assignee = models.ForeignKey(UserProfile, related_name='tasks_assigned')
    completed_by = models.ForeignKey(
        UserProfile, related_name='tasks_completed', null=True
    )
    completed_date = models.DateField(null=True)

    due_date = models.DateField()

    def get_next_assignee(self):
        participants = list(self.task.participants.all())
        try:
            i = participants.index(self.assignee)
        except ValueError:
            # unexpected, but could happen if assignee was removed
            # from task participants
            return random.choice(participants)

        i = (i + 1) % len(participants)
        return participants[i]

    def complete(self, userprofile):
        self.completed_by = userprofile
        self.completed_date = datetime.date.today()

    def create_next(self):
        """
        Create the next due instance of this task. No-op
        if the associated task is not recurring.

        """
        frequency = self.task.frequency
        if frequency == Task.DAILY:
            delta = datetime.timedelta(days=1)
        elif frequency == Task.WEEKLY:
            delta = datetime.timedelta(weeks=1)
        elif frequency == Task.MONTHLY:
            delta = datetime.timedelta(days=30)
        elif frequency == Task.YEARLY:
            delta = datetime.timedelta(weeks=52)
        else:
            return None

        new_instance = TaskInstance.objects.create(
            task=self.task,
            assignee=self.get_next_assignee(),
            due_date=self.due_date + delta
        )

        return new_instance

    def __str__(self):
        return "%s assigned to %s" % (
            self.task.title, str(self.assignee)
        )
