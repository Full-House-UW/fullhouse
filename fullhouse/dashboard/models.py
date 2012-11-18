import datetime
import hashlib
import random

from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site

from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now as datetime_now

from registration.models import SHA1_RE

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
    zip_code = models.CharField(max_length=9)

    def __str__(self):
        return self.name


class InviteManager(models.Manager):

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
                invite.activation_key = self.model.INVITE_ACCEPTED
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
        invite_profile = self.create(house=house,
                           email=email,
                           invite_key=invite_key,
                           sent_date=datetime_now())

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

    house = models.ForeignKey(House)
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

    user = models.OneToOneField(User, related_name='profile')
    birthday = models.DateField(null=True)
    # should perhaps be a ManyToManyField, but for simplicity, we'll only allow
    # one house per person for now.
    house = models.ForeignKey(
        House, related_name='members', null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.user.__str__()


class Announcement(models.Model):
    creator = models.ForeignKey(UserProfile)
    text = models.TextField()
    house = models.ForeignKey(House, related_name='announcements')
    expiration = models.DateField(null=True)

    def __str__(self):
        return self.creator.__str__() + ": " + self.text

    class Meta:
        ordering = ['-id']
