from django.conf import settings
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site

from django.contrib.auth.models import User
from django.template.loader import (
    get_template, render_to_string
)

from emailusernames.utils import migrate_usernames


encountered_emails = set()
duplicates = {}


def update_duplicate_email(user):
    email = user.email
    username = user._username
    email_name, domain_part = email.rsplit('@', 1)
    email_name = '%s+%s' % (email_name, username)
    user.email = '@'.join([email_name, domain_part])
    user.save()


def send_email_update_notification(user):
    if Site._meta.installed:
        site = Site.objects.get_current()
    else:
        site = RequestSite(request)

    ctx_dict = {'username': user._username,
                'updated_email': user.email,
                'site': site}
    subject = render_to_string("auth_update_subject.txt", ctx_dict)
    subject = ''.join(subject.splitlines())
    message = render_to_string("auth_update_email.txt", ctx_dict)
    user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)


def migrate_fullhouse_usernames():
    """
        WARNING: RUN THIS SCRIPT BEFORE SOUTH MIGRATIONS OR BAD
        SHIT WILL HAPPEN.

    """

    for user in User.objects.all().order_by('date_joined'):
        email = str(user.email)
        if email in encountered_emails:
            username = user._username
            update_duplicate_email(user)
            send_email_update_notification(user)
            if email in duplicates:
                duplicates[email].append(user.email)
            else:
                duplicates[email] = [user.email]
        else:
              encountered_emails.update([email])

    print "Updated duplicate emails for %d of %d accounts" % (
          sum(len (d) for d in (duplicates.values())), len(encountered_emails))

    migrate_usernames()



