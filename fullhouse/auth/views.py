from django.http import HttpResponseRedirect
from django.contrib.auth import views as auth_views
from registration import views as registration_views

from functools import wraps


def login(request, *args, **kwargs):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/dashboard/')
    return auth_views.login(request, *args, **kwargs)


def register(request, *args, **kwargs):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/dashboard/')
    return registration_views.register(request, *args, **kwargs)


def password_reset(request, *args, **kwargs):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/password/change/')
    return auth_views.password_reset(request, *args, **kwargs)
